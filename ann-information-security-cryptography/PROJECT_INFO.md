# Project information

| | |
|---|---|
| **Title** | A Survey on Information Security Using Artificial Neural Network |
| **Degree** | Bachelor of Science (Honours), Computer Science |
| **Semester / paper code** | Semester VI, CMSA DSE-VI |
| **Project authors** | Arka Maity, Debjit Dey, Shouvik Sarkar |
| **Supervisor** | Dr. Soumya Paul |
| **Institution** | Ramakrishna Mission Vivekananda Centenary College, Rahara, Khardaha, West Bengal 700118 |
| **Report date** | April 2024 |
| **Full report** | [docs/project-report.pdf](docs/project-report.pdf) |

This repository packages the Python algorithm from the report with a web interface, a command-line tool, automated tests, CI and Docker support. The report's chapters are covered here and in [docs/survey.md](docs/survey.md) (background, literature survey, applications, bibliography) and [docs/algorithm.md](docs/algorithm.md) (algorithm, example, sample output).

## Objectives

The report sets three objectives for a symmetric-key cryptographic system built on a feed-forward neural architecture:

1. **Enhanced data confidentiality** — a dynamic, hard-to-predict encryption process that makes unauthorised decryption difficult.
2. **Robust message authentication** — verify the origin of a message and prevent tampering, so that integrity is kept and forgery is prevented.
3. **Long-distance network resilience** — work across diverse networks, tolerate delays and handle varying packet sizes.

## Requirements (SRS)

- **Functional:** a key-generation module, an encryption module and a decryption module. The encryption module conceals the information; the decryption module decodes it at the recipient's end.
- **Non-functional:** security, reliability, performance under heavy load, maintainability, scalability and usability.
- **Goal:** confidentiality and authenticity of messages exchanged between computer systems, protecting against eavesdropping and tampering.

## Feasibility study

- **Technical feasibility** — does the team have the skills, and is the engineering complexity manageable?
- **Behavioural feasibility** — how will users react to the new system, and does it need training or changes in how they work?

## Schedule (2024)

| Task | Start | End |
|---|---|---|
| Problem definition and literature survey | 10 Jan | 1 Feb |
| Analysis (algorithm and flowchart) | 7 Feb | 14 Feb |
| Design | 8 Feb | 8 Mar |
| Coding | 14 Feb | 17 Apr |
| Testing | 11 Mar | 15 Apr |
| User write-up / manual | 8 Feb | 20 Apr |

## Tools

Python · Windows 11 · MS Project (schedule and Gantt chart) · MS Word (report).

## Testing

The report names three kinds of testing: white-box testing (tests designed from the internal structure), unit testing (modules in isolation) and integration testing (modules combined). In this repository they map to the `pytest` suite in `tests/`:

- **Unit tests** — key generation, XOR, the eight nodes, token validation, hexadecimal keys.
- **Integration tests** — encrypt → token → decrypt, the command-line tool and the web app.
- **Reference tests** — the three console runs printed in the report, and a comparison with the report's original source code (`tests/report_reference.py`) on random messages.

The suite runs on every push through GitHub Actions.

## Conclusion of the report and scope of this repository

The report concludes that neural-network approaches show potential for strengthening encryption and for detecting security threats. The code in this repository implements only the encryption heuristic; threat detection is covered by the survey but not implemented, and message authentication is an objective that the code does not implement. See the limitations in [docs/algorithm.md](docs/algorithm.md#9-limitations).

## Future scope (from the report)

- Add asymmetric cryptography as a basis for secure communication between the parties involved in a computation.
- Build more complex mathematical functions into the network architecture to improve its processing for specific tasks.
- Generate nodes dynamically so that the network can adapt its structure while it runs.
