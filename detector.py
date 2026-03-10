import os
import time
import cv2
import numpy as np
from mss import mss
from PIL import Image

from config import (
    MODELO,
    CONFIANCA_MINIMA,
    MONITOR,
    ESCALA_JANELA,
    ESPESSURA_BORDA,
    TAMANHO_FONTE,
    MOSTRAR_INFO,
    FILTRAR_CLASSES,
    GRAVAR_VIDEO,
    NOME_VIDEO,
    FPS_GRAVACAO,
    SOM_AO_DETECTAR,
)


class DetectorDeTela:
    def __init__(self):
        from ultralytics import YOLO

        print("Carregando modelo YOLO:", MODELO)
        self.modelo = YOLO(MODELO)
        self.sct = mss()
        self.cores = self._gerar_cores(80)
        self.gravador = None

        print("Pronto. Aperte ESC para sair.")

    def _gerar_cores(self, n):
        np.random.seed(42)
        return [tuple(int(c) for c in np.random.randint(100, 255, size=3)) for _ in range(n)]

    def _capturar(self):
        monitor = self.sct.monitors[MONITOR]
        shot = self.sct.grab(monitor)
        frame = np.array(Image.frombytes("RGB", (shot.width, shot.height), shot.rgb))
        return frame

    def _detectar(self, frame):
        r = self.modelo(frame, verbose=False)[0]
        dets = []
        for box in r.boxes:
            conf = float(box.conf[0])
            if conf < CONFIANCA_MINIMA:
                continue

            cls_id = int(box.cls[0])
            cls_name = self.modelo.names[cls_id]

            if FILTRAR_CLASSES and cls_name not in FILTRAR_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            dets.append((cls_id, cls_name, conf, (x1, y1, x2, y2)))
        return dets

    def _desenhar(self, frame, dets):
        for cls_id, cls_name, conf, (x1, y1, x2, y2) in dets:
            cor = self.cores[cls_id % len(self.cores)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, ESPESSURA_BORDA)

            label = f"{cls_name} {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, TAMANHO_FONTE, 2)
            cv2.rectangle(frame, (x1, y1 - th - 12), (x1 + tw + 8, y1), cor, -1)
            cv2.putText(
                frame,
                label,
                (x1 + 4, y1 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                TAMANHO_FONTE,
                (255, 255, 255),
                2,
            )
        return frame

    def _hud(self, frame, fps, count, infer_ms):
        if not MOSTRAR_INFO:
            return frame
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (330, 105), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        cv2.putText(frame, f"FPS: {fps:.0f}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Objetos: {count}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Inferencia: {infer_ms:.0f}ms", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        return frame

    def _beep(self):
        if SOM_AO_DETECTAR and os.name == "nt":
            import winsound
            winsound.Beep(1000, 80)

    def iniciar(self):
        fps = 0
        frames = 0
        t_fps = time.time()
        t_beep = 0

        while True:
            frame = self._capturar()

            t0 = time.time()
            dets = self._detectar(frame)
            infer_ms = (time.time() - t0) * 1000.0

            frame = self._desenhar(frame, dets)

            frames += 1
            if time.time() - t_fps >= 1.0:
                fps = frames
                frames = 0
                t_fps = time.time()

            frame = self._hud(frame, fps, len(dets), infer_ms)

            h, w = frame.shape[:2]
            nw, nh = int(w * ESCALA_JANELA), int(h * ESCALA_JANELA)
            show = cv2.resize(frame, (nw, nh))
            show = cv2.cvtColor(show, cv2.COLOR_RGB2BGR)

            if GRAVAR_VIDEO:
                if self.gravador is None:
                    fourcc = cv2.VideoWriter_fourcc(*"XVID")
                    self.gravador = cv2.VideoWriter(NOME_VIDEO, fourcc, FPS_GRAVACAO, (nw, nh))
                self.gravador.write(show)

            if dets and SOM_AO_DETECTAR and (time.time() - t_beep) > 2:
                self._beep()
                t_beep = time.time()

            cv2.imshow("Detector de Objetos - Tela", show)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        if self.gravador:
            self.gravador.release()
            print("Video salvo em:", NOME_VIDEO)

        cv2.destroyAllWindows()


if __name__ == "__main__":
    DetectorDeTela().iniciar()