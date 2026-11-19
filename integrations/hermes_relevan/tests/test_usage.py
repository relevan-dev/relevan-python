from hermes_relevan.usage import RecalledHit, used_results

HITS = [
    RecalledHit(
        "obsidian:proxmox-1",
        0,
        "Proxmox backup plan",
        "Nightly vzdump of every VM to the Synology NAS at 02:00, zstd compression, rclone to B2.",
    ),
    RecalledHit(
        "obsidian:pihole-2",
        1,
        "Pi-hole and Unbound",
        "Pi-hole runs on the Raspberry Pi with Unbound as the recursive resolver on port 5335.",
    ),
    RecalledHit(
        "obsidian:dal-3",
        2,
        "Weeknight dal",
        "Red lentils simmered with turmeric, then a tarka of cumin seeds and garlic.",
    ),
]


def test_a_cited_id_is_grade_two() -> None:
    used = used_results(HITS, "how do I back up?", "Per [obsidian:proxmox-1], it runs at 02:00.")
    assert [(u.hit.object_id, u.grade) for u in used] == [("obsidian:proxmox-1", 2)]


def test_a_named_title_is_grade_two() -> None:
    used = used_results(HITS, "what do I cook?", "Make the weeknight dal tonight.")
    assert [(u.hit.object_id, u.grade) for u in used] == [("obsidian:dal-3", 2)]


def test_a_paraphrase_is_grade_one() -> None:
    reply = "Your VMs are dumped nightly to the Synology with zstd, and rclone copies them offsite."
    used = used_results(HITS, "how are my backups done?", reply)
    assert [(u.hit.object_id, u.grade) for u in used] == [("obsidian:proxmox-1", 1)]


def test_echoing_the_question_does_not_count() -> None:
    question = "does unbound on the raspberry resolver use port 5335?"
    used = used_results(HITS, question, "Yes: unbound, raspberry, resolver, port 5335.")
    assert used == []


def test_an_unrelated_reply_uses_nothing() -> None:
    assert used_results(HITS, "what's the weather?", "I cannot check the weather.") == []
    assert used_results(HITS, "anything", "   ") == []


def test_an_id_inside_a_longer_id_does_not_count() -> None:
    hits = [RecalledHit("product:a-1", 0, "", "")]
    assert used_results(hits, "q", "See [product:a-12] instead.") == []


def test_an_id_counts_only_inside_square_brackets() -> None:
    hits = [RecalledHit("1", 0, "", ""), RecalledHit("2", 1, "", "")]
    assert used_results(hits, "q", "I can suggest 1 option, or 2.") == []
    used = used_results(hits, "q", "Two notes say so [1, 2].")
    assert [(u.hit.object_id, u.grade) for u in used] == [("1", 2), ("2", 2)]


def test_a_weak_paraphrase_next_to_a_strong_one_does_not_count() -> None:
    hits = [
        RecalledHit(
            "paperless:11",
            0,
            "Home insurance policy 2026",
            "Allianz home insurance policy number HX-4471-209. Building cover, excess 250 EUR.",
        ),
        RecalledHit(
            "paperless:15",
            1,
            "Car insurance renewal",
            "Allianz motor insurance renewal for the Skoda Octavia, policy MX-88120. "
            "Premium 612 EUR.",
        ),
    ]
    reply = (
        "The Skoda Octavia is insured with Allianz under policy number MX-88120, and the "
        "motor insurance renewal premium is 612 EUR."
    )
    used = used_results(hits, "Which car is insured with Allianz?", reply)
    assert [(u.hit.object_id, u.grade) for u in used] == [("paperless:15", 1)]
