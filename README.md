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

The habit that comes with it: I measure before I decide, and I write the reasoning down. Every claim
in the projects below has a number behind it in the repo — a benchmark, a test count, a table of
what the other approach actually did when I tried it.

<sub>Bengaluru, India · open to interesting problems</sub>

---

## Selected work

### juno-assistant

`Python` &nbsp;`QML` &nbsp;`sherpa-onnx` &nbsp;`faster-whisper` &nbsp;`Kokoro TTS`

> An offline wake-word voice assistant for Omarchy. Say the name, and Claude answers out loud —
> with a live overlay of everything it does.

**The measurement that redesigned it.** The first version matched the wake word inside a Whisper
transcript. That is the wrong tool: Whisper is a language model, so handed an unfamiliar proper noun
it rewrites it into whatever English is likelier — "Juno" came back as *"You know."* Measured in one
room, the two approaches:

| | Whisper transcript matching | Dedicated wake model |
| :-- | :-- | :-- |
| Wake phrase, 3 attempts | **0 / 3** — one returned *"I know your post is amazing"* | **3 / 3** at 0.94–0.99 |
| 90 s of room noise, nobody speaking | 45 transcriptions, all discarded | **0 false wakes, 0 transcriptions** |
| Idle cost | a 3–13 s transcription of every noise burst | ~10–15% of one core, constant |

So Whisper no longer runs at all while idle — a continuously-listening detector sits ahead of the
VAD, and the transcriber only wakes when it does.

**Trading latency for being understood.** Once woken, the command goes to the `small` model rather
than the fast one, because in a real room the fast one invents sentences: the same audio transcribed
as *"We need certain amount of time to get here"* by `base` and *"Can you set an alarm at 10:00?"* by
`small`. That costs about 8 seconds instead of 3 — paid only on the path a human is waiting on, never
on the idle path that runs all day.

**Shape.** Two processes over one socket. The overlay is a pure subscriber: close it mid-answer and
the answer still finishes, and the wake word keeps working with no UI open at all. `jarvis enroll`
fits a personal wake classifier on a dozen recordings of your voice in about three minutes on CPU,
reports a held-out ROC AUC so you can see whether it generalised, and votes *alongside* the shipped
model — so enrolling can only add detections, never remove them.

**[→ Read the write-up](https://github.com/sarthax10/juno-assistant)**

<br>

### tessera

`C#` &nbsp;`.NET 10` &nbsp;`WebSockets` &nbsp;`CRDT` &nbsp;`MIT`

> A real-time collaborative canvas. Several people draw on one board at once, from different
> machines, over unreliable networks — and every replica ends up showing the same picture.

**Why it's hard.** Three requirements pull against each other. Two replicas that have seen the same
edits must show the same document, in whatever order those edits arrived. A drag has to render on
the next frame — 16.7 ms — while a round trip to `us-east-1` is 30–80 ms. And a client that loses the
network has to keep working, then rejoin without losing or duplicating anything. The second forces
every edit to apply locally before the server has seen it, which forces a real merge strategy,
because two people will always change the same thing before either learns about the other.

**How it works.** Hybrid logical clocks, so one machine with a fast clock can't win every conflict
forever and one with a slow clock can't lose every one — both failures are silent otherwise.
Fractional base-62 indexing, so reordering a shape rewrites one key instead of renumbering hundreds.
One actor per board, so convergence bugs can't hide inside a lock. Add-wins deletion, because a shape
that wrongly survives costs one keystroke, and one wrongly removed may be work you never get back.

**How it's tested.** Convergence is checked as a property, not by example: a generated 400-operation
session across three replicas, replayed in 200 random delivery orders, every ordering required to
produce a byte-identical document. 80 tests, warnings as errors.

<sub>**Status** — server-side done and runnable · browser client next · Postgres and AWS after that</sub>

**[→ Read the design notes](https://github.com/sarthax10/tessera)** &nbsp;·&nbsp; [ARCHITECTURE.md](https://github.com/sarthax10/tessera/blob/master/ARCHITECTURE.md) covers the wire protocol, and why not OT, why not Yjs

<br>

### rackwm

`Rust` &nbsp;`Win32` &nbsp;`7 crates` &nbsp;`event-driven`

> A native Windows tiling window manager in the spirit of Hyprland — built directly on Win32, not a
> port of a Linux tool.

**Why it's hard.** Windows offers no compositor hook you can politely ask for tiling. It is all event
plumbing: open, close, focus, drag — reacted to as they happen, with no polling loop anywhere in the
process. The overlays have to track windows they don't own, in real time, without stealing focus from
them.

**How it works.** `rackwm-engine` tiles the primary monitor into a grid and draws its own chrome — a
rounded animated glow around the focused window, a dim overlay on every other tiled one.
`rackwm-panel` is a separate native control panel for gaps, opacity, glow colour and animation
duration; it writes straight to `%APPDATA%\rackwm\rackwm.toml`, which the engine hot-reloads through
a file watcher. Five supporting crates keep config, theme, platform, UI and core apart.

<sub>**Status** — engine and panel usable · hotkeys still hardcoded (<code>Alt+Shift+Q/J/K/C</code>) · configurable keybindings next</sub>

**[→ Read the architecture](https://github.com/sarthax10/rackwm)**

<br>

<details>
<summary><b>Everything else worth a look</b></summary>

<br>

| Project | Stack | What it is |
| :-- | :-- | :-- |
| **[urbanConnect](https://github.com/sarthax10/urbanConnect)** | `C#` `JS` `Clerk` | Home-services booking platform. Slots are generated from service duration against each professional's day, so two customers can't be sold the same hour; roles are assigned on first sign-in and gate every dashboard route. |
| **[textEditor](https://github.com/sarthax10/textEditor)** | `Rust` | A text editor from first principles — another "just import it" primitive I wanted to understand from the inside. |
| **[BlazeBin](https://github.com/sarthax10/BlazeBin)** | `Node` `Express` `EJS` | Server-rendered snippet-sharing app. <!-- TODO: confirm this one-liner --> |
| **[SuperChat](https://github.com/sarthax10/SuperChat)** · **[VideoChat](https://github.com/sarthax10/VideoChat)** | `JS` | Earlier real-time experiments, text and video — the ones that led to caring how shared state actually converges. |

</details>

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
