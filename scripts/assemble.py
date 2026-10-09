#!/usr/bin/env python3
"""Assemble a video from per-beat clips + a full voiceover track.

Each beat in the timing manifest maps one narration sentence to one clip.
Clips are joined with crossfades; the fade-overlap math keeps the final
video exactly as long as the voiceover (see docs/05-assembly.md).

Manifest format (JSON list):
    {"beat": 1, "sentence": "...", "start": 0.0, "end": 4.2,
     "duration": 4.2, "clip": "beat-01.mp4"}

Usage:
    python3 assemble.py --manifest beats.json --clips ./clips --vo narration.mp3 --out final.mp4
"""
import argparse, json, math, os, subprocess, sys

FADE = 0.35
W, H, FPS = 1920, 1080, 30

def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--clips", required=True)
    ap.add_argument("--vo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    beats = json.load(open(a.manifest))
    missing = [b["beat"] for b in beats
               if not os.path.exists(os.path.join(a.clips, b["clip"]))]
    if missing:
        print(f"ABORT: {len(missing)} beats missing clips: {missing[:10]}")
        sys.exit(2)

    clips = [os.path.join(a.clips, b["clip"]) for b in beats]
    durs = [b["duration"] for b in beats]
    # Fade-overlap math: clip i covers d_i + FADE (except the first),
    # so the xfade chain yields exactly sum(d_i) — the VO length.
    needs = [durs[0]] + [d + FADE for d in durs[1:]]
    SRC_FPS = 24

    fc = []
    for i, need in enumerate(needs):
        cd = probe_dur(clips[i])
        have = int(round(cd * SRC_FPS))
        want = int(math.ceil(need * SRC_FPS))
        loop_f = ""
        if have < want:  # loop short clips at filter level (never -stream_loop)
            loop_f = f"loop=loop={math.ceil(want / have) - 1}:size={have},"
        fc.append(f"[{i}:v]{loop_f}trim=0:{need:.3f},setpts=PTS-STARTPTS,"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},fps={FPS}[v{i}]")
    prev, out_dur = "v0", needs[0]
    for i in range(1, len(needs)):
        off = out_dur - FADE
        fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={FADE}:"
                  f"offset={off:.3f}[x{i}]")
        prev, out_dur = f"x{i}", out_dur + needs[i] - FADE
    fc.append(f"[{prev}]format=yuv420p[vout]")
    n = len(clips)
    fc.append(f"[{n}:a]atrim=0:{out_dur:.3f},asetpts=PTS-STARTPTS,loudnorm[aout]")

    cmd = ["ffmpeg", "-y"]
    for c in clips:
        cmd += ["-i", c]
    cmd += ["-i", a.vo, "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-c:a", "aac", "-b:a", "128k", a.out]
    print(f"Assembling {n} clips -> {a.out} (~{out_dur:.0f}s)")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAILED:"); print(r.stderr[-2000:]); sys.exit(1)
    print("Done.")

if __name__ == "__main__":
    main()
