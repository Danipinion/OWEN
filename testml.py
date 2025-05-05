import unittest
from main import predict_and_analyze, train_model 

class TestPredictionFunction(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        # Asumsikan train_model mengembalikan model dan feature_columns yang valid
        self.model, self.feature_columns = train_model()
        # Pastikan model dan feature_columns tidak None sebelum menjalankan tes lain
        if self.model is None or self.feature_columns is None:
            self.skipTest("Model training failed, skipping prediction tests.")

    def test_ideal_conditions(self):
        """Test when all conditions are within ideal ranges."""
        data = {'suhu': 27, 'kelembaban': 70, 'kekeruhan': 3, 'ph': 7.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 1)
        self.assertEqual(analysis['status'], 'ideal')
        self.assertEqual(analysis['reasons'], [])

    def test_high_temperature(self):
        """Test when temperature is above the ideal range."""
        data = {'suhu': 32, 'kelembaban': 70, 'kekeruhan': 3, 'ph': 7.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 0)
        self.assertEqual(analysis['status'], 'tidak ideal')
        self.assertIn('Suhu tidak ideal (32°C)', analysis['reasons'])

    def test_low_humidity(self):
        """Test when humidity is below the ideal range."""
        data = {'suhu': 27, 'kelembaban': 55, 'kekeruhan': 3, 'ph': 7.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 0)
        self.assertEqual(analysis['status'], 'tidak ideal')
        self.assertIn('Kelembaban tidak ideal (55%)', analysis['reasons'])

    def test_high_turbidity(self):
        """Test when turbidity is above the ideal range."""
        data = {'suhu': 27, 'kelembaban': 70, 'kekeruhan': 8, 'ph': 7.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 0)
        self.assertEqual(analysis['status'], 'tidak ideal')
        self.assertIn('Kekeruhan terlalu tinggi (8 NTU)', analysis['reasons'])

    def test_acidic_ph(self):
        """Test when pH is below the ideal range."""
        data = {'suhu': 27, 'kelembaban': 70, 'kekeruhan': 3, 'ph': 6.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 0)
        self.assertEqual(analysis['status'], 'tidak ideal')
        self.assertIn('pH tidak ideal (6.0)', analysis['reasons'])

    def test_alkaline_ph(self):
        """Test when pH is above the ideal range."""
        data = {'suhu': 27, 'kelembaban': 70, 'kekeruhan': 3, 'ph': 8.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 0)
        self.assertEqual(analysis['status'], 'tidak ideal')
        self.assertIn('pH tidak ideal (8.0)', analysis['reasons'])

    def test_multiple_non_ideal_conditions(self):
        """Test when multiple conditions are outside ideal ranges."""
        data = {'suhu': 35, 'kelembaban': 50, 'kekeruhan': 10, 'ph': 5.5}
        prediction, analysis = predict_and_analyze(data)
        self.assertEqual(prediction, 0)
        self.assertEqual(analysis['status'], 'tidak ideal')
        self.assertIn('Suhu tidak ideal (35°C)', analysis['reasons'])
        self.assertIn('Kelembaban tidak ideal (50%)', analysis['reasons'])
        self.assertIn('Kekeruhan terlalu tinggi (10 NTU)', analysis['reasons'])
        self.assertIn('pH tidak ideal (5.5)', analysis['reasons'])

    def test_missing_data(self):
        """Test with missing data (should handle gracefully)."""
        data = {'suhu': 27, 'ph': 7.0} # Missing kelembaban and kekeruhan
        prediction, analysis = predict_and_analyze(data)
        # Prediksi mungkin tidak akurat karena data kurang, tetapi tidak boleh error
        self.assertIsInstance(analysis, dict)
        self.assertIn('status', analysis)

    def test_model_not_trained(self):
        """Test when the model hasn't been trained (setUp failed)."""
        # Force model dan feature_columns menjadi None untuk simulasi
        global model, feature_columns
        original_model = model
        original_feature_columns = feature_columns
        model = None
        feature_columns = None
        data = {'suhu': 27, 'kelembaban': 70, 'kekeruhan': 3, 'ph': 7.0}
        prediction, analysis = predict_and_analyze(data)
        self.assertIsNone(prediction)
        self.assertEqual(analysis['status'], 'error')
        self.assertIn('Model belum dilatih', analysis['message'])
        global model, feature_columns
        model = original_model
        feature_columns = original_feature_columns

if __name__ == '__main__':
    unittest.main()