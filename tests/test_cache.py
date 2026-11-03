import unittest
from music_experiments.cache import cache_digest, source_row_indices


class CacheIdentityTests(unittest.TestCase):
    def test_dictionary_order_does_not_change_identity(self):
        self.assertEqual(cache_digest({"seed": 7, "model": "a"}), cache_digest({"model": "a", "seed": 7}))

    def test_reordered_rows_invalidate_cache(self):
        self.assertNotEqual(cache_digest({"ids": ["a", "b"]}), cache_digest({"ids": ["b", "a"]}))

    def test_model_and_dataset_changes_invalidate_cache(self):
        base = {"model": "a", "fingerprint": "v1", "labels": [0, 1]}
        for change in ({"model": "b"}, {"fingerprint": "v2"}, {"labels": [1, 0]}):
            self.assertNotEqual(cache_digest(base), cache_digest({**base, **change}))

    def test_skipped_audio_keeps_caption_alignment(self):
        captions = ["first", "unreadable audio", "third"]
        kept = source_row_indices([{"i": 0}, {"i": 2}], len(captions))
        self.assertEqual(captions[kept[1]], "third")

    def test_invalid_and_duplicate_rows_are_rejected(self):
        for meta in ([{"i": -1}], [{"i": 3}], [{"i": True}], [{"i": 0}, {"i": 0}]):
            with self.assertRaises(ValueError):
                source_row_indices(meta, 3)


if __name__ == "__main__":
    unittest.main()
