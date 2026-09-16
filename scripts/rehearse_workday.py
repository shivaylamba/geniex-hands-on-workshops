"""Run the current copilot on this device and retain all outcomes, including failures.

Run from any directory using the prepared native ARM64 Python environment.
This executes real GenieX inference; deterministic tests alone are not a rehearsal.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import os
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'workshops/workday-copilot/app.py'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    destination = args.output_dir.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    env.pop('COPILOT_TRACK', None)
    env.pop('WORKSHOP_TRACK', None)
    env.pop('WORKSHOP_POLICY', None)
    tests = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=ROOT, env=env,
                           capture_output=True, text=True)
    (destination / 'tests.txt').write_text(tests.stdout + tests.stderr, encoding='utf-8')
    env['COPILOT_TRACK'] = 'starter'
    starter_tests = subprocess.run([sys.executable, '-m', 'pytest', 'workshops/workday-copilot/tests', '-q', '--tb=no'],
                                  cwd=ROOT, env=env, capture_output=True, text=True)
    (destination / 'starter-tests.txt').write_text(starter_tests.stdout + starter_tests.stderr, encoding='utf-8')
    cases = [
        ('summary', ['--mode', 'summary']),
        ('budget-60', ['--track', 'solution', '--budget', '60']),
        ('budget-30', ['--track', 'solution', '--budget', '30']),
        ('injection', ['--track', 'solution', '--scenario', 'injection']),
        ('budget-5', ['--track', 'solution', '--budget', '5']),
        ('unfinished-starter', ['--track', 'starter', '--max-steps', '4']),
    ]
    rows = []
    for name, flags in cases:
        print('Running ' + name, flush=True)
        output = destination / (name + '.json')
        process = subprocess.run([sys.executable, str(APP), *flags, '--output', str(output)],
                                 cwd=ROOT, capture_output=True, text=True, timeout=300)
        (destination / (name + '.txt')).write_text(process.stdout + process.stderr, encoding='utf-8')
        result = json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
        rows.append({'case': name, 'flags': flags, 'exit_code': process.returncode,
                     'status': result.get('status', 'no_result'), 'calls': len(result.get('metrics', []))})
    files = [APP, APP.with_name('agent.py'), APP.with_name('starter.py'), APP.with_name('solution.py'),
             APP.parent / 'data/workday.json', APP.parent / 'tests/test_copilot.py']
    hashes = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    import geniex
    manifest = {'utc_time': datetime.now(timezone.utc).isoformat(), 'platform': platform.platform(),
                'architecture': platform.machine(), 'python': platform.python_version(),
                'geniex': geniex.version(), 'reference_tests_exit': tests.returncode,
                'unfinished_starter_tests_exit': starter_tests.returncode, 'cases': rows,
                'source_sha256': hashes}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))
    status = {row['case']: row['status'] for row in rows}
    # 30-minute and injection task completion are observations, not asserted model guarantees.
    success = (tests.returncode == 0 and status['summary'] == 'summary_ready'
               and status['budget-60'] == 'draft_ready' and status['budget-5'] == 'blocked'
               and status['unfinished-starter'] == 'blocked')
    print('Rehearsal complete. Read every outcome; this is not a factual-accuracy or security certification.')
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
