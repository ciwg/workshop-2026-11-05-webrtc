class: center, middle

# Why does browser video need a relay?

## WebRTC and TURN, in five minutes

JJ Salley<br>
CSWG · November 5, 2026

???
Hello. This is a short explanation of one surprising part of browser video:
why two people who can both reach the internet may still need a third machine
in the middle.

---

## The simple picture

```text
  your browser  ───────────────►  their browser
       camera        video             screen
```

**The hope:** the two browsers connect directly.

???
At first glance, a video call looks like one browser sending media directly to
another. WebRTC is the browser technology that tries to make that happen. When
the direct route works, it is efficient: the media does not need to pass
through the application server.

---

## The real picture

```text
  browser A                         browser B
      │                                 │
  home / office                     home / office
  router + firewall                 router + firewall
      │                                 │
      └────────── public internet ──────┘
```

**The problem:** each network decides what incoming traffic it will accept.

???
Most people are behind a home router, office firewall, mobile carrier, or some
combination. Those devices protect their networks by refusing unexpected
incoming traffic. So being online does not automatically mean that one browser
can reach another browser directly.

---

## WebRTC tries the direct routes first

```text
 browser A ── asks / answers ── browser B
     │                              │
     └────── tries possible paths ──┘
                 │
               STUN
          “What route can I use?”
```

**STUN helps discover routes. It cannot guarantee a direct route exists.**

???
The application helps the browsers exchange connection information. Then WebRTC
tries the routes it can discover. A STUN service can tell a browser how its
network appears from outside. That often helps a direct connection work, but it
cannot make every firewall or network policy allow one.

---

## TURN is the reliable fallback

```text
 browser A ──►  TURN relay  ──► browser B
      ▲             ▲              ▲
      └──────── both can reach it ─┘
```

**If direct media is blocked, both browsers send through the relay.**

???
TURN is that relay. Instead of requiring browser A to accept an incoming route
from browser B, both browsers make outbound connections to one reachable TURN
server. The server relays the encrypted media between them. It is not the
first choice, but it is what makes a call reliable across the networks where a
direct path fails.

---

## That means another implementation layer

```text
 meeting app       WebRTC in browsers        TURN service
 ───────────       ──────────────────        ────────────
 consent           capture + connection      public reachability
 invitations       direct-route attempts     short-lived credentials
 room rules        send / receive media      bandwidth + limits
 signaling                                      monitoring + rotation
```

**The app is not the relay. The relay is not the app.**

???
This is the important point. A meeting application decides things such as
consent, invitations, and room rules. Browsers capture and render media. A
TURN service is separate infrastructure: it has to be reachable, authenticated,
limited, monitored, and operated. Building media features therefore means more
than writing the visible application.

---

## Why does a project need a TURN relay?

```text
 direct path works?  ── yes ──► use it
        │
        no
        ▼
 relay path works?   ── yes ──► the call still works
        │
        no
        ▼
 show a clear failure instead of pretending the call connected
```

**A TURN relay makes “works for people on different networks” a realistic goal.**

???
Without TURN, a demo can work beautifully on one local network and still fail
for real people elsewhere. TURN does not make every problem disappear, and it
does not replace good application design. It supplies the network fallback
that browser media needs when direct connectivity is unavailable. The relay
could be a managed service or an operator-run, prebuilt TURN service; this talk
does not choose between those options.

---

class: center, middle

# Thank you.

???
Thank you. I am happy to take questions.

---

class: center, middle

# Questions only — not part of the talk

## How might a project obtain TURN?

```text
 managed TURN service       operator-run prebuilt TURN service
 ────────────────────       ─────────────────────────────────
 provider operates it       team operates a standard TURN package
 usage / vendor tradeoffs   control / operations tradeoffs
                 │                 │
                 └──── both provide a standard relay endpoint ────┘
```

???
Only use this slide if someone asks how the relay would be obtained. The
five-minute talk does not select a provider or require a custom relay. Either
path still needs authenticated, short-lived credentials and a responsible
operator; the tradeoff is who carries the operational work.

---

class: center, middle

# Questions only — not part of the talk

## Does TURN read the call?

```text
 browser A  ══ encrypted media ══►  TURN  ══ encrypted media ══►  browser B
```

TURN relays packets. It is not the meeting application's authority for
consent, invitations, or room membership.

???
TURN moves packets; it does not decide who should be in a meeting. The meeting
application still owns those decisions. The exact privacy properties depend on
the media and deployment design, so avoid making broader claims than that in a
short talk.
