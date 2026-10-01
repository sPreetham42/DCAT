import json
import urllib.request


def test_all():
    url_scenarios = "http://localhost:8000/api/scenarios"
    res_sc = urllib.request.urlopen(url_scenarios)
    data_sc = json.loads(res_sc.read().decode("utf-8"))
    scenarios = data_sc["scenarios"]

    print(f"Loaded {len(scenarios)} built-in scenarios.\n")

    for sc in scenarios:
        payload = {
            "sender": sc["sender"],
            "subject": sc["subject"],
            "body": sc["body"],
            "image_b64": sc["image_b64"],
        }
        req = urllib.request.Request(
            "http://localhost:8000/api/analyze",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        res = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

        mod = res["modality"].upper()
        lbl = res["simulated_label"]
        prob = int(res["simulated_spam_probability"] * 100)
        exec_steps = [s["name"] for s in res["pipeline_steps"] if s["status"] == "executed"]
        skip_steps = [s["name"] for s in res["pipeline_steps"] if s["status"] == "skipped"]

        print(f"=== {sc['title']} ===")
        print(f"  Route Selected    : {mod}")
        print(f"  Simulated Outcome : {lbl} ({prob}%)")
        print(f"  Executed Steps    : {exec_steps}")
        print(f"  Skipped Steps     : {skip_steps}")
        print(f"  Explanation       : {res['explanation']}")
        print(f"  Computation Saved : {res['computation_saved_description']}")
        print()


if __name__ == "__main__":
    test_all()
