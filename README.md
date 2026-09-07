<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/sarthax10/sarthax10/main/assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/sarthax10/sarthax10/main/assets/hero-light.svg">
    <img alt="Shreyansh Sarthak — software engineer in Bengaluru, India. I build systems from the protocol up. Rust, C#, Python." src="https://raw.githubusercontent.com/sarthax10/sarthax10/main/assets/hero-dark.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="#selected-work" title="Three projects, in depth">Work</a>
  &nbsp;·&nbsp;
  <a href="#how-i-build" title="Stack, grouped by layer">Stack</a>
  &nbsp;·&nbsp;
  <a href="#now" title="What's on the bench right now">Now</a>
  &nbsp;·&nbsp;
  <a href="#elsewhere" title="Ways to reach me">Contact</a>
</p>

<br>

Lately I've been building things that usually arrive as a dependency — a CRDT merge engine, a tiling
window manager for Windows, a wake-word voice assistant. Not because the libraries are bad. Because
building one is the only reliable way to find out where it breaks, and which of its guarantees were
never guarantees at all.

The habit that comes with it: I measure before I decide, and I write the reasoning down. Every
design call in those repos has a number behind it — a benchmark, a test count, a table of what the
approach I rejected actually did when I tried it.

<sub>Bengaluru, India · open to interesting problems</sub>

---

## Selected work

Short versions — the full write-ups live in each repo.

| Project | What it is |
| :-- | :-- |
| **[juno-assistant](https://github.com/sarthax10/juno-assistant)**<br><sub>`Python` `QML`</sub> | Offline wake-word voice assistant. A dedicated detector runs ahead of the transcriber, so Whisper stays switched off until you actually call it. |
| **[tessera](https://github.com/sarthax10/tessera)**<br><sub>`C#` `.NET 10`</sub> | Real-time collaborative canvas on a CRDT merge engine written from scratch — hybrid logical clocks, fractional indexing, convergence tested as a property rather than by example. |
| **[rackwm](https://github.com/sarthax10/rackwm)**<br><sub>`Rust` `Win32`</sub> | Native Windows tiling window manager. Event-driven with no polling loop, its own focus-glow overlay, and a config the engine hot-reloads as you edit it. |
| **[urbanConnect](https://github.com/sarthax10/urbanConnect)**<br><sub>`C#` `JS`</sub> | Home-services booking platform. Slots are generated per professional per day, so two customers can't be sold the same hour. |
| **[textEditor](https://github.com/sarthax10/textEditor)**<br><sub>`Rust`</sub> | A text editor from first principles. |
| **[BlazeBin](https://github.com/sarthax10/BlazeBin)** · **[SuperChat](https://github.com/sarthax10/SuperChat)** · **[VideoChat](https://github.com/sarthax10/VideoChat)**<br><sub>`Node` `JS`</sub> | Earlier web work — snippet sharing, and real-time text and video chat. |

---

## How I build

Grouped by the layer it lives at, rather than by how many logos fit on a line.

| Layer | What I reach for |
| :-- | :-- |
| **Systems** | Rust · C# · .NET · C · C++ — concurrency, protocol design, event-driven daemons |
| **Web** | TypeScript · JavaScript · Blazor · React · Next.js · Tailwind |
| **Data & ML** | SQL Server · Postgres · MySQL · SQLite · MongoDB · Python · NumPy · PyTorch |
| **Design** | Figma · Illustrator · After Effects — the reason my READMEs have their own artwork |
| **Everyday** | Git · Linux · Vercel · Firebase |

<details>
<summary><sub>Also shipped with, less often</sub></summary>

<br>

Angular · Vue · Nuxt · Express · Bootstrap · QML / Qt · GitLab · Photoshop · Lightroom · GIMP ·
Canva · Notion

</details>

---

## Now

- **Building** — [juno-assistant](https://github.com/sarthax10/juno-assistant): personal wake-word enrolment, and getting the false-wake rate down without raising the miss rate
- **Next** — the TypeScript client for [tessera](https://github.com/sarthax10/tessera), against a merge engine that's already done and tested
- **Then** — swapping tessera's in-memory repository for Postgres, and a real keybinding table for [rackwm](https://github.com/sarthax10/rackwm) so the chords stop being hardcoded
- **Reading up on** — distributed systems verification: how you convince yourself a merge is correct, rather than merely untested

<sub>Last updated September 2026</sub>

---

## Signals

What I actually write, measured across every public repository — not a scoreboard.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/sarthax10/sarthax10/main/assets/languages-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/sarthax10/sarthax10/main/assets/languages-light.svg">
    <img alt="Language distribution across public repositories: C# 31%, Python 21%, Rust 17%, JavaScript 17%, QML 9%, other 5%." src="https://raw.githubusercontent.com/sarthax10/sarthax10/main/assets/languages-dark.svg" width="560">
  </picture>
</p>

---

## Elsewhere

<p align="center">
  <a href="mailto:shreyanshsarthak10@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-16202B?style=flat-square&labelColor=16202B&logo=maildotru&logoColor=C99A3F"></a>
  &nbsp;
  <a href="https://linkedin.com/in/shreyansh-sarthak"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-16202B?style=flat-square&labelColor=16202B&logo=linkedin&logoColor=C99A3F"></a>
  &nbsp;
  <a href="https://instagram.com/sarthax10"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-16202B?style=flat-square&labelColor=16202B&logo=instagram&logoColor=C99A3F"></a>
</p>

<p align="center">
  <sub><i>If it looks like magic, I want to know where it breaks.</i></sub>
</p>
