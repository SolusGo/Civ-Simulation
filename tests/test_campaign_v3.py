"""Run a cheap deterministic campaign and verify invariants without requiring a winner."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class CampaignSmokeTest(unittest.TestCase):
    def test_short_seeded_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            cmd=[sys.executable,str(ROOT/'engine/sim56_v3.py'),'--seed','345',
                 '--max-turn','17','--snapshot-every','6','--output-dir',tmp]
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
            self.assertEqual(result.returncode,0,result.stderr)
            data=json.loads((Path(tmp)/'war56_v3_results.json').read_text())
            self.assertEqual(data['seed'],345)
            self.assertEqual(data['endturn'],17)
            self.assertEqual([s['turn'] for s in data['snapshots']],[0,6,12,17])
            self.assertIsNone(data['winner'])
            self.assertEqual(len(data['roster']),56)
            for snap in data['snapshots']:
                self.assertEqual(len(snap['statistics']),56)
                self.assertEqual(len(snap['city_owners']),len(snap['city_ids']))
                self.assertTrue(all(i>=0 for i in snap['city_owners']))
                for st in snap['statistics']:
                    self.assertGreaterEqual(st['army'],0)
                    self.assertLessEqual(st['momentum'],6)
                    self.assertLessEqual(st['roster_alive'],5)

if __name__=="__main__": unittest.main()
