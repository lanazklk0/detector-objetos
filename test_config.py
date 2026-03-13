import unittest

import config


class ConfigImportTest(unittest.TestCase):
    def test_config_module_exposes_expected_settings(self):
        self.assertEqual(config.MODELO, "yolov8n.pt")
        self.assertEqual(config.CONFIANCA_MINIMA, 0.45)
        self.assertEqual(config.MONITOR, 1)
        self.assertEqual(config.ESCALA_JANELA, 0.5)
        self.assertEqual(config.ESPESSURA_BORDA, 2)
        self.assertEqual(config.TAMANHO_FONTE, 0.6)
        self.assertTrue(config.MOSTRAR_INFO)
        self.assertEqual(config.FILTRAR_CLASSES, [])
        self.assertFalse(config.GRAVAR_VIDEO)
        self.assertEqual(config.NOME_VIDEO, "gravacao.avi")
        self.assertEqual(config.FPS_GRAVACAO, 15)
        self.assertFalse(config.SOM_AO_DETECTAR)


if __name__ == "__main__":
    unittest.main()
