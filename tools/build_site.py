#!/usr/bin/env python3
"""Build the static KS Lawn Ranger site from site.config.json and the copy below.

Run from the repo root: python3 tools/build_site.py
"""

import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://kslawnranger.com"
PHONE_DISPLAY = "(913) 221-7981"
PHONE_TEL = "+19132217981"
EMAIL = "kslawnranger@gmail.com"
REVIEW_URL = "https://g.page/r/CQ3hgayPFJW2EBM/review"
FORM_ACTION = "https://formspree.io/f/mrblvwde"
GA_ID = "G-G26464Y3JF"
YEAR = date.today().year
LASTMOD = date.today().isoformat()

CONFIG = json.loads((ROOT / "site.config.json").read_text())
MANIFEST = json.loads((ROOT / "images" / "manifest.json").read_text())

CORE_AREAS = [
    ("Manhattan", "/areas/manhattan-ks/", "The largest city on the route, with weekly mowing, cleanups, installs, and snow for homes and businesses."),
    ("Alma", "/areas/alma-ks/", "Home base. Owner-operated service for in-town lots and properties toward the Flint Hills."),
    ("Wamego", "/areas/wamego-ks/", "On the way between Alma and Manhattan, with mature trees and heavy fall leaf cleanup."),
    ("St. George", "/areas/st-george-ks/", "A small Highway 24 town on the same drive, including newer lawns that need a steady cut."),
    ("Junction City", "/areas/junction-city-ks/", "Residential and commercial properties, including seasonal snow contracts."),
    ("Ogden", "/areas/ogden-ks/", "Just west of Manhattan and part of that side of the route."),
]
NEARBY = ("Westmoreland", "Paxico")
AREA_SENTENCE = (
    "KS Lawn Ranger LLC is based in Alma and serves Manhattan, Alma, Wamego, "
    "St. George, Junction City, and Ogden. Westmoreland and Paxico are nearby areas — "
    "send the address and we will confirm."
)

FORM_SERVICES = [
    "Weekly mowing route",
    "Lawn mowing & edging",
    "Spring & fall cleanup / leaf removal",
    "Landscaping install",
    "Hardscaping",
    "Mulch & rock install",
    "Sod installation",
    "Bush & shrub trimming",
    "Bed weeding & maintenance",
    "Aeration",
    "Overseeding",
    "Snow removal & ice management",
    "Seasonal snow contract",
    "Other",
]

NAV = [
    ("Services", "/services/"),
    ("Service area", "/#service-area"),
    ("Gallery", "/gallery/"),
    ("About", "/about/"),
    ("FAQ", "/faq/"),
    ("Contact", "/contact/"),
]

FAQS = [
    (
        "How do you price lawn mowing?",
        "Pricing depends on lot size, obstacles, and how much trimming the property needs. Most residential visits are quoted after a quick on-site look. Text your address for a free estimate. We do not publish a price list.",
    ),
    (
        "Do you offer weekly mowing?",
        "Yes. Weekly and bi-weekly mowing are available, depending on the season and how the lawn is growing. Ask for a weekly mowing route when you request a quote.",
    ),
    (
        "Do you bag clippings?",
        "Mulching is standard. Bagging can be requested and included in the quote when you want clippings removed.",
    ),
    (
        "When should I aerate and overseed in Kansas?",
        "Fall is the best window, typically September through October. Cooler weather and fall moisture help new roots establish before winter.",
    ),
    (
        "How often should a lawn be aerated?",
        "Most lawns do well with core aeration once a year in the fall. Lawns with heavy clay soil or a lot of foot traffic may benefit from a second visit. Leave the plugs on the lawn. They break down and return material to the soil.",
    ),
    (
        "Do you haul away debris?",
        "Yes. Spring and fall cleanups, leaf removal, and shrub trimming can include haul-away of leaves, sticks, branches, and lawn waste. The work area is left tidy.",
    ),
    (
        "When should I schedule a spring cleanup?",
        "Most properties schedule spring cleanup between March and May, depending on weather and how early things start growing. Fall leaf removal is scheduled as the leaves come down.",
    ),
    (
        "Do you offer free estimates?",
        "Yes. Estimates are free and there is no obligation. Call, text, or send the quote form with your address and the services you want.",
    ),
    (
        "What areas do you serve?",
        AREA_SENTENCE,
    ),
    (
        "Are you insured?",
        "Yes. KS Lawn Ranger LLC is fully insured. Proof of insurance is available on request.",
    ),
    (
        "What payment methods do you accept?",
        "Cash, check, Venmo, and a QuickBooks payment link. Invoices are available on request. Estimates and billing are handled in QuickBooks.",
    ),
    (
        "Do you work on commercial properties?",
        "Yes. Weekly mowing, bed maintenance, seasonal cleanups, landscaping, and snow removal are available for commercial properties as well as homes. Seasonal snow contracts are available for businesses that want to be on the route before the first storm.",
    ),
    (
        "Do you guarantee bare pavement after snow removal?",
        "No. Weather, refreeze, compaction, and drifting can leave surfaces slippery. Snow service focuses on clearing what is present at the time of the visit and opening safe access.",
    ),
    (
        "Do you offer ice melt or salting?",
        "Yes. Ice melt or salt can be added per visit or included in an agreed snow plan. Pre-treatment is available by request when the weather allows.",
    ),
    (
        "What are your hours?",
        "Monday through Saturday, 7:00 AM to 6:00 PM. Sunday is closed. Call or text (913) 221-7981 during those hours.",
    ),
    (
        "Who runs KS Lawn Ranger?",
        "KS Lawn Ranger LLC is owner-operated by Kohlton and based in Alma, Kansas. The phone and email on this site reach the business directly.",
    ),
]


def esc(value):
    return html.escape(str(value), quote=True)


def picture(slug, alt, sizes, eager=False, position="center"):
    info = MANIFEST[slug]
    variants = info["variants"]
    big = variants[-1]
    webp = ", ".join(f"{v['webp']} {v['w']}w" for v in variants)
    jpg = ", ".join(f"{v['jpg']} {v['w']}w" for v in variants)
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    style = f' style="object-position:{esc(position)}"' if position != "center" else ""
    return (
        "<picture>"
        f'<source type="image/webp" srcset="{webp}" sizes="{esc(sizes)}">'
        f'<img src="{big["jpg"]}" srcset="{jpg}" sizes="{esc(sizes)}" '
        f'width="{big["w"]}" height="{big["h"]}" alt="{esc(alt)}" '
        f'loading="{loading}" decoding="async"{priority}{style}>'
        "</picture>"
    )


def largest_jpg(slug):
    return ORIGIN + MANIFEST[slug]["variants"][-1]["jpg"]


def logo():
    variant = MANIFEST["logo"]["variants"][0]
    return (
        f'<img src="{variant["jpg"]}" width="{variant["w"]}" height="{variant["h"]}" '
        'alt="KS Lawn Ranger LLC">'
    )


def crumbs(items):
    if not items:
        return ""
    parts = ['<p class="crumbs">']
    for i, (label, href) in enumerate(items):
        if i:
            parts.append(" / ")
        if href:
            parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
        else:
            parts.append(esc(label))
    parts.append("</p>")
    return "".join(parts)


def breadcrumb_schema(items, path):
    elements = [{"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"}]
    position = 2
    for label, href in items:
        if not href:
            href = path
        elements.append(
            {"@type": "ListItem", "position": position, "name": label, "item": ORIGIN + href}
        )
        position += 1
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}


def local_business():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": ORIGIN + "/#business",
        "name": "KS Lawn Ranger LLC",
        "url": ORIGIN + "/",
        "image": [largest_jpg("first-one"), ORIGIN + "/images/opt/logo.png"],
        "logo": ORIGIN + "/images/opt/logo.png",
        "telephone": "+1-913-221-7981",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Alma",
            "addressRegion": "KS",
            "addressCountry": "US",
        },
        "areaServed": [
            {"@type": "City", "name": name + ", KS"} for name, _, _ in CORE_AREAS
        ],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                ],
                "opens": "07:00",
                "closes": "18:00",
            }
        ],
        "paymentAccepted": "Cash, Check, Venmo, QuickBooks payment link",
        "founder": {"@type": "Person", "name": "Kohlton", "jobTitle": "Owner"},
        "sameAs": [REVIEW_URL],
    }


def service_schema(name, path, description):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": name,
        "description": description,
        "url": ORIGIN + path,
        "provider": {"@id": ORIGIN + "/#business"},
        "areaServed": [{"@type": "City", "name": name_ + ", KS"} for name_, _, _ in CORE_AREAS],
    }


def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in FAQS
        ],
    }


def json_ld(*blocks):
    return "\n".join(
        '<script type="application/ld+json">\n'
        + json.dumps(block, ensure_ascii=False)
        + "\n</script>"
        for block in blocks
        if block
    )


def promo_bar():
    promo = CONFIG.get("promo") or {}
    if not promo.get("enabled") or not promo.get("text"):
        return ""
    href = promo.get("href") or "/contact/"
    return (
        f'<div class="promo"><a href="{esc(href)}">{esc(promo["text"])}</a></div>'
    )


def header(current, quote_href):
    desktop = []
    for label, href in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        desktop.append(f'<a href="{esc(href)}"{current_attr}>{esc(label)}</a>')
    desktop.append(
        f'<a class="header-phone" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>'
    )
    desktop.append(
        f'<a class="btn btn-primary header-quote" href="{esc(quote_href)}">Get a Free Quote</a>'
    )
    mobile_main = []
    for label, href in NAV:
        mobile_main.append(f'<a href="{esc(href)}">{esc(label)}</a>')
    mobile_main.append(f'<a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>')
    mobile_main.append(f'<a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a>')
    mobile_main.append(f'<a href="{esc(quote_href)}">Get a Free Quote</a>')
    service_links = "".join(
        f'<a href="{esc(href)}">{esc(label)}</a>'
        for label, href in SERVICE_LINKS
    )
    return f"""
<header class="header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="KS Lawn Ranger home">{logo()}</a>
    <nav class="nav-desktop" aria-label="Primary">{''.join(desktop)}</nav>
    <a class="header-call" href="tel:{PHONE_TEL}">Call</a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mobileNav">Menu</button>
  </div>
</header>
<div class="nav-mobile" id="mobileNav">
  <nav aria-label="Mobile">
    {''.join(mobile_main)}
    <div class="nav-sub">{service_links}</div>
  </nav>
</div>
"""


def footer():
    services = "".join(
        f'<li><a href="{esc(href)}">{esc(label)}</a></li>' for label, href in SERVICE_LINKS
    )
    areas = "".join(
        f'<li><a href="{esc(href)}">{esc(name)}, KS</a></li>' for name, href, _ in CORE_AREAS
    )
    return f"""
<footer class="footer">
  <div class="wrap footer-grid">
    <div>
      <h2>KS Lawn Ranger LLC</h2>
      <p>Owner-operated by Kohlton. Based in Alma, Kansas.</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br>
      <a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a><br>
      <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>Monday–Saturday 7:00 AM – 6:00 PM<br>Sunday closed</p>
      <p>Fully insured. Proof on request.<br>Cash, check, Venmo, and QuickBooks payment link.</p>
    </div>
    <div>
      <h2>Services</h2>
      <ul>{services}</ul>
    </div>
    <div>
      <h2>Service area</h2>
      <ul>{areas}</ul>
      <p>Nearby: {NEARBY[0]} and {NEARBY[1]}. Send your address to confirm.</p>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/gallery/">Project gallery</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/commercial/">Commercial services</a></li>
        <li><a href="{REVIEW_URL}" rel="noopener noreferrer">Google reviews</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">
    <p>{esc(AREA_SENTENCE)}</p>
    <p>© {YEAR} KS Lawn Ranger LLC. All rights reserved.</p>
  </div>
</footer>
"""


def sticky(quote_href):
    return f"""
<div class="sticky-cta" role="region" aria-label="Quick contact">
  <a class="btn btn-green" href="tel:{PHONE_TEL}">Call</a>
  <a class="btn btn-primary" href="{esc(quote_href)}">Get a Quote</a>
</div>
"""


def quote_form(source, precheck=None, property_type=None, heading="Request a free quote", intro=None):
    if intro is None:
        intro = "Tell us about the property. Estimates are free. Kohlton follows up by phone, text, or email — whichever you pick below."
    checks = []
    for label in FORM_SERVICES:
        checked = " checked" if precheck and label == precheck else ""
        checks.append(
            f'<label class="check"><input type="checkbox" name="services" value="{esc(label)}"{checked}>'
            f"<span>{esc(label)}</span></label>"
        )
    def radio(name, value, text, selected):
        checked = " checked" if selected else ""
        return (
            f'<label class="choice"><input type="radio" name="{name}" value="{esc(value)}" required{checked}>'
            f"<span>{esc(text)}</span></label>"
        )
    res = radio("property_type", "Residential", "Residential", property_type == "Residential")
    com = radio("property_type", "Commercial", "Commercial", property_type == "Commercial")
    methods = "".join(
        radio("contact_method", value, value, False) for value in ("Phone", "Text", "Email")
    )
    return f"""
<section class="section section-white" id="quote">
  <div class="wrap split split-form">
    <div>
      <p class="eyebrow">Free estimate</p>
      <h2>{esc(heading)}</h2>
      <p>{esc(intro)}</p>
      <p><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><br>
      <a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a><br>
      <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="fine">Monday–Saturday, 7:00 AM – 6:00 PM. Fully insured, proof on request.</p>
    </div>
    <form class="quote-form form-card" action="{FORM_ACTION}" method="POST" accept-charset="UTF-8">
      <p class="fine">Fields marked required must be filled in. This sends a quote request. No price is collected on the form.</p>
      <div class="form-error" tabindex="-1" role="alert"></div>
      <input type="hidden" name="_redirect" value="{ORIGIN}/thank-you.html">
      <input type="hidden" name="_subject" value="Quote request from kslawnranger.com">
      <input type="hidden" name="source_page" value="{esc(source)}">
      <div class="hp" aria-hidden="true">
        <label>Company website <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
      </div>
      <div class="form-grid">
        <label class="field">Full name
          <input name="name" autocomplete="name" required minlength="2" maxlength="80" pattern=".*[A-Za-z].*" title="Enter your name">
        </label>
        <div class="grid-2">
          <label class="field">Phone
            <input name="phone" type="tel" inputmode="tel" autocomplete="tel" required minlength="7" maxlength="30">
          </label>
          <label class="field">Email
            <input name="email" type="email" autocomplete="email" required maxlength="120">
          </label>
        </div>
        <label class="field">Property address
          <input name="address" autocomplete="street-address" required minlength="5" maxlength="160" placeholder="Street, city">
        </label>
        <fieldset style="border:0;padding:0;margin:0">
          <legend style="font-weight:700;color:var(--ink)">Property type</legend>
          <div class="choice-row">{res}{com}</div>
        </fieldset>
        <fieldset style="border:0;padding:0;margin:0">
          <legend style="font-weight:700;color:var(--ink)">Services</legend>
          <div class="check-grid">{''.join(checks)}</div>
        </fieldset>
        <fieldset style="border:0;padding:0;margin:0">
          <legend style="font-weight:700;color:var(--ink)">Preferred contact method</legend>
          <div class="choice-row">{methods}</div>
        </fieldset>
        <label class="field">Message <span class="fine">optional</span>
          <textarea name="message" maxlength="2000" placeholder="Lot details, timing, or anything we should know"></textarea>
        </label>
        <button class="btn btn-primary" type="submit">Get a Free Quote</button>
        <p class="fine">The form is sent to KS Lawn Ranger and is used to reply about your estimate.</p>
      </div>
    </form>
  </div>
</section>
"""


def area_list():
    items = []
    for name, href, note in CORE_AREAS:
        items.append(f'<a href="{esc(href)}">{esc(name)}, KS <span>View</span></a>')
    return (
        '<ul class="area-list">'
        + "".join(f"<li>{item}</li>" for item in items)
        + "</ul>"
        + f'<p class="nearby"><strong>Nearby areas.</strong> {NEARBY[0]} and {NEARBY[1]} are not core stops. '
        "Send the address and we will tell you if we can take the property.</p>"
    )


def related(links):
    cards = []
    for label, href, text in links:
        cards.append(
            f'<a class="plain-card" href="{esc(href)}"><h3>{esc(label)}</h3><p>{esc(text)}</p></a>'
        )
    return f'<div class="grid-3" style="margin-top:1.5rem">{"".join(cards)}</div>'


def actions(quote="#quote"):
    return f"""
<div class="actions">
  <a class="btn btn-primary" href="{esc(quote)}">Get a Free Quote</a>
  <a class="btn btn-green" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
  <a class="btn btn-ghost" href="sms:{PHONE_TEL}">Text</a>
</div>
"""


def head(page):
    path = page["path"]
    canonical = ORIGIN + path
    robots = page.get("robots", "index, follow")
    image = page.get("image", largest_jpg("first-one"))
    title = page["title"]
    description = page["description"]
    preload = ""
    if page.get("preload"):
        slug = page["preload"]
        variants = MANIFEST[slug]["variants"]
        srcset = ", ".join(f"{v['webp']} {v['w']}w" for v in variants)
        preload = (
            f'<link rel="preload" as="image" href="{variants[-1]["webp"]}" type="image/webp" '
            f'imagesrcset="{srcset}" imagesizes="(min-width: 980px) 46vw, 100vw">'
        )
    schemas = [local_business()]
    if page.get("crumbs"):
        schemas.append(breadcrumb_schema(page["crumbs"], path))
    if page.get("service_name"):
        schemas.append(service_schema(page["service_name"], path, description))
    if page.get("faq"):
        schemas.append(faq_schema())
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{esc(robots)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(image)}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="KS Lawn Ranger LLC">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{esc(image)}">
<meta name="theme-color" content="#6e1730">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/css/site.css">
{preload}
{json_ld(*schemas)}
</head>
"""


def render(page):
    quote_href = page.get("quote_href", "#quote" if page.get("form") else "/contact/#quote")
    main = page["main"]
    form = ""
    if page.get("form"):
        form = quote_form(
            page["path"],
            precheck=page.get("precheck"),
            property_type=page.get("property_type"),
            heading=page.get("form_heading", "Request a free quote"),
            intro=page.get("form_intro"),
        )
    doc = (
        head(page)
        + "<body class=\"has-sticky\">\n"
        + '<a class="skip" href="#main">Skip to content</a>\n'
        + promo_bar()
        + header(page.get("nav", ""), quote_href)
        + f'<main id="main">{main}{form}</main>'
        + footer()
        + sticky(quote_href)
        + '<script src="/js/site.js" defer></script>\n'
        + analytics()
        + "</body></html>\n"
    )
    return doc


def analytics():
    return f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
"""


def write_page(page):
    path = page["path"]
    if path.endswith(".html"):
        dest = ROOT / path.lstrip("/")
    elif path == "/":
        dest = ROOT / "index.html"
    else:
        dest = ROOT / path.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render(page))
    return dest


def redirect(old, new, label):
    dest = ROOT / old.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page moved | KS Lawn Ranger</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{ORIGIN}{new}">
<meta http-equiv="refresh" content="0; url={new}">
<link rel="icon" href="/favicon.ico">
</head>
<body>
<p>This page has moved. <a href="{new}">{html.escape(label)}</a>.</p>
</body>
</html>
"""
    )


def hero_block(eyebrow, title, lede, image, alt, eager=True):
    return f"""
<section class="hero wrap">
  <div class="hero-copy">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {actions()}
    <ul class="trust">
      <li>Owner-operated</li>
      <li>Fully insured</li>
      <li>Mon–Sat 7am–6pm</li>
      <li>Free on-site estimates</li>
    </ul>
  </div>
  <div class="hero-media">{picture(image, alt, "(min-width: 980px) 46vw, 100vw", eager=eager)}</div>
</section>
"""


def service_shell(copy):
    body_image = picture(
        copy["image"],
        copy["image_alt"],
        "(min-width: 980px) 42vw, 100vw",
        eager=True,
    )
    return f"""
<article class="wrap page-hero">
  {crumbs(copy["crumbs"])}
  <div class="split">
    <div>
      <p class="eyebrow">{esc(copy["eyebrow"])}</p>
      <h1>{copy["h1"]}</h1>
      <p class="lede">{copy["lede"]}</p>
      {actions()}
    </div>
    <div class="media">{body_image}</div>
  </div>
</article>
<section class="section wrap prose">
  {copy["body"]}
  <h2>Where this work is done</h2>
  <p>{esc(AREA_SENTENCE)}</p>
  <h2>Related services</h2>
  {related(copy["related"])}
</section>
"""


# --- Page copy ----------------------------------------------------------------

SERVICE_LINKS = [
    ("Lawn mowing", "/services/lawn-mowing/"),
    ("Spring & fall cleanup", "/services/spring-fall-cleanup/"),
    ("Landscaping installs", "/services/landscaping/"),
    ("Hardscaping", "/services/hardscaping/"),
    ("Mulch & rock", "/services/mulch-rock/"),
    ("Sod installation", "/services/sod/"),
    ("Shrub trimming", "/services/shrub-trimming/"),
    ("Bed maintenance", "/services/bed-maintenance/"),
    ("Aeration", "/services/aeration/"),
    ("Overseeding", "/services/overseeding/"),
    ("Snow removal", "/services/snow-removal/"),
    ("Residential snow", "/services/snow-removal-residential/"),
    ("Commercial snow", "/services/snow-removal-commercial/"),
    ("Commercial services", "/commercial/"),
]


def comparisons(limit=None):
    rows = CONFIG["comparisons"] if limit is None else CONFIG["comparisons"][:limit]
    blocks = []
    for item in rows:
        before = picture(item["before"], item["alt_before"], "(min-width: 800px) 520px, 100vw")
        after = picture(item["after"], item["alt_after"], "(min-width: 800px) 520px, 100vw")
        blocks.append(
            f"""
<div data-ba>
  <div class="ba">
    {after}
    <div class="ba-after">{before}</div>
    <span class="ba-label ba-label-before">Before</span>
    <span class="ba-label ba-label-after">After</span>
    <input type="range" min="0" max="100" value="54" aria-label="Show more of the before or after photo">
  </div>
  <p class="ba-caption">{esc(item["caption"])}</p>
</div>
"""
        )
    return "\n".join(blocks)


def testimonials():
    cards = []
    for item in CONFIG["testimonials"]:
        cards.append(
            f"""
<blockquote class="quote-block">
  <p class="stars" aria-hidden="true">★★★★★</p>
  <p>“{esc(item["quote"])}”</p>
  <footer>{esc(item["place"])}</footer>
</blockquote>
"""
        )
    return f'<div class="grid-3">{"".join(cards)}</div>'


def home_main():
    cards = [
        ("stripes", "Weekly mowing & edging", "A steady cut, trimmed edges, and hard surfaces blown clear.", "/services/lawn-mowing/", "Mowing stripes on a residential lawn"),
        ("leaves", "Spring & fall cleanup", "Leaf removal, bed cleanup, and haul-away when the season turns.", "/services/spring-fall-cleanup/", "Leaves piled for haul-away"),
        ("mulch", "Landscaping installs", "Beds, mulch, rock, sod, and the work that makes a yard look finished.", "/services/landscaping/", "Fresh mulch bed with stepping stones"),
        ("hardscaping", "Hardscaping", "Patios and retaining walls, quoted on site before anything is built.", "/services/hardscaping/", "Paver patio beside a rock bed"),
        ("after-5-fixed", "Mulch & rock", "Bed prep and a clean edge, then mulch or decorative rock.", "/services/mulch-rock/", "Rock installed in a side yard"),
        ("sod", "Sod installation", "Site prep and new sod so a bare or tired area can establish.", "/services/sod/", "Newly laid sod in a backyard"),
        ("after-4-fixed", "Shrub trimming", "Hedges and foundation shrubs shaped, with clippings hauled away.", "/services/shrub-trimming/", "Shaped foundation hedge"),
        ("after-6", "Bed weeding", "Weeds pulled, edges cut, and beds kept from disappearing into the lawn.", "/services/bed-maintenance/", "Mulched foundation bed"),
        ("aeration", "Aeration", "Core aeration in the fall so water and air can reach the roots.", "/services/aeration/", "Aeration plugs on a lawn"),
        ("overseeding", "Overseeding", "Seed worked into thin lawns, best paired with fall aeration.", "/services/overseeding/", "Young grass filling in"),
        ("snow-removal", "Snow & ice", "Residential and commercial clearing, plus seasonal snow contracts.", "/services/snow-removal/", "Driveway cleared after snow"),
    ]
    card_html = []
    for image, title, text, href, alt in cards:
        card_html.append(
            f"""
<a class="card" href="{href}">
  <div class="card-media">{picture(image, alt, "(min-width: 980px) 30vw, (min-width: 760px) 45vw, 100vw")}</div>
  <div class="card-body"><h3>{esc(title)}</h3><p>{esc(text)}</p><span class="card-link">See the service</span></div>
</a>
"""
        )
    return f"""
{hero_block(
    "Alma, Kansas · Owner-operated",
    "Lawn care for Manhattan and the towns around it.",
    "KS Lawn Ranger LLC handles weekly mowing, landscaping installs, spring and fall cleanup, and snow removal for homes and businesses. Kohlton runs the company from Alma.",
    "first-one",
    "Striped lawn in front of a house maintained by KS Lawn Ranger",
)}
<section class="section section-white" id="services">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Services</p>
        <h2>Work you can book for the whole year.</h2>
      </div>
      <a href="/services/">All services</a>
    </div>
    <div class="cards">{''.join(card_html)}</div>
  </div>
</section>
<section class="section section-green">
  <div class="wrap split">
    <div>
      <p class="eyebrow" style="color:#e7c7c7">Commercial</p>
      <h2>Properties that need a route, not a one-time favor.</h2>
      <p>Offices, storefronts, and other commercial lots can go on a weekly mowing route. Seasonal snow contracts put a business on the list before the first storm. Invoices are available, and billing can go through QuickBooks.</p>
      <div class="actions">
        <a class="btn btn-on-dark" href="/commercial/">Commercial services</a>
        <a class="btn btn-line-light" href="/services/snow-removal-commercial/">Commercial snow</a>
      </div>
    </div>
    <div class="grid-2">
      <div class="plain-card"><h3>Weekly mowing route</h3><p>Same visit pattern through the growing season, with edging and blow-off included.</p></div>
      <div class="plain-card"><h3>Seasonal snow contract</h3><p>Agreed surfaces, ice melt when it is part of the plan, and a contact who already knows the property.</p></div>
      <div class="plain-card"><h3>Insured</h3><p>KS Lawn Ranger LLC is fully insured. Proof is available on request before work starts.</p></div>
      <div class="plain-card"><h3>Direct</h3><p>Call or text {PHONE_DISPLAY}. The company is owner-operated by Kohlton.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Recent work</p>
        <h2>Before and after, from real jobs.</h2>
      </div>
      <a href="/gallery/">Full gallery</a>
    </div>
    <div class="grid-2">{comparisons(2)}</div>
  </div>
</section>
<section class="section section-white">
  <div class="wrap">
    <p class="eyebrow">How a quote works</p>
    <h2>Four steps. No price list to guess from.</h2>
    <div class="grid-4 steps" style="margin-top:1rem">
      <div class="plain-card step"><strong>1. Ask</strong><p>Call, text, or send the form with the address and the services you need.</p></div>
      <div class="plain-card step"><strong>2. Look</strong><p>Most quotes follow a quick on-site look at size, access, and how much trimming or haul-away is involved.</p></div>
      <div class="plain-card step"><strong>3. Quote</strong><p>You get the scope before work is scheduled. Nothing on this site is a published price.</p></div>
      <div class="plain-card step"><strong>4. Do the work</strong><p>Mowing, an install, a cleanup, or snow — then the property is left tidy.</p></div>
    </div>
  </div>
</section>
<section class="section" id="reviews">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Reviews</p>
        <h2>Notes from homeowners, and the live Google list.</h2>
      </div>
      <a href="{REVIEW_URL}" rel="noopener noreferrer">Leave a Google review</a>
    </div>
    <p class="muted">These three comments are the testimonials already published on this site. For the current Google list, use the reviews below or open Google directly. We do not print a review count here.</p>
    {testimonials()}
    <div id="google-reviews" class="reviews-embed"></div>
  </div>
</section>
<section class="section section-white" id="service-area">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Service area</p>
      <h2>Six towns. The same standard in each.</h2>
      <p>{esc(AREA_SENTENCE)}</p>
      <p>Hours are Monday through Saturday, 7:00 AM to 6:00 PM.</p>
    </div>
    <div>{area_list()}</div>
  </div>
</section>
"""


def services_index_main():
    items = []
    blurbs = {href: blurb for href, blurb in SERVICE_BLURBS}
    for label, href in SERVICE_LINKS:
        items.append(
            f'<a class="plain-card" href="{esc(href)}"><h3>{esc(label)}</h3><p>{esc(blurbs.get(href, ""))}</p></a>'
        )
    return f"""
<article class="wrap page-hero prose">
  {crumbs([("Services", None)])}
  <p class="eyebrow">Services</p>
  <h1>Mowing, installs, cleanup, and snow.</h1>
  <p class="lede">Every service below is quoted for the property in front of us. Weekly mowing routes and seasonal snow contracts are called out on the form so a repeat visit is easy to request.</p>
  {actions("#quote")}
</article>
<section class="section wrap">
  <div class="cards">{''.join(items)}</div>
  <p style="margin-top:1.5rem">{esc(AREA_SENTENCE)}</p>
</section>
"""


SERVICE_BLURBS = [
    ("/services/lawn-mowing/", "Weekly or bi-weekly cuts, trimming, edging, and blow-off. Mulching is standard."),
    ("/services/spring-fall-cleanup/", "Leaf removal, bed cleanup, sticks, and haul-away in spring and fall."),
    ("/services/landscaping/", "Install work: beds, mulch, rock, sod, and plantings quoted as one project."),
    ("/services/hardscaping/", "Patios and retaining walls. The scope is set at the on-site quote."),
    ("/services/mulch-rock/", "Prep, a defined edge, then mulch or decorative rock."),
    ("/services/sod/", "Ground prepared and sod laid so a new lawn can establish."),
    ("/services/shrub-trimming/", "Hedges and shrubs shaped. Haul-away can be included."),
    ("/services/bed-maintenance/", "Weeding, edging, and upkeep so beds stay separate from the lawn."),
    ("/services/aeration/", "Core aeration, ideally in September and October."),
    ("/services/overseeding/", "Seed for thin turf, strongest when it follows aeration."),
    ("/services/snow-removal/", "Clearing and ice management for homes and businesses."),
    ("/services/snow-removal-residential/", "Driveways, walks, and steps. Per visit or a seasonal plan."),
    ("/services/snow-removal-commercial/", "Entrances and agreed areas, with seasonal contracts and invoices."),
    ("/commercial/", "Mowing routes, bed work, cleanups, and snow for commercial properties."),
]


def gallery_main():
    figures = []
    for item in CONFIG["gallery"]:
        big = MANIFEST[item["image"]]["variants"][-1]["jpg"]
        figures.append(
            f"""
<figure data-cat="{esc(item["cat"])}">
  <button type="button" data-full="{esc(big)}" data-alt="{esc(item["alt"])}">
    {picture(item["image"], item["alt"], "(min-width: 1100px) 30vw, (min-width: 760px) 45vw, 100vw")}
  </button>
  <figcaption>{esc(item["caption"])}</figcaption>
</figure>
"""
        )
    return f"""
<article class="wrap page-hero">
  {crumbs([("Gallery", None)])}
  <p class="eyebrow">Projects</p>
  <h1>Photos from the work, not a stock library.</h1>
  <p class="lede">These are project photos already used by KS Lawn Ranger. Drag the comparisons to see the change. If a photo is not labeled with a town, we have not assigned one.</p>
</article>
<section class="section wrap">
  <h2>Before and after</h2>
  <div class="grid-2">{comparisons()}</div>
  <h2>All project photos</h2>
  <div class="filters" role="toolbar" aria-label="Filter photos">
    <button type="button" data-filter="all" aria-pressed="true">All</button>
    <button type="button" data-filter="mowing" aria-pressed="false">Mowing</button>
    <button type="button" data-filter="landscape" aria-pressed="false">Landscape</button>
    <button type="button" data-filter="cleanup" aria-pressed="false">Cleanup</button>
    <button type="button" data-filter="lawn" aria-pressed="false">Aeration & seed</button>
    <button type="button" data-filter="snow" aria-pressed="false">Snow</button>
  </div>
  <div class="gallery">{''.join(figures)}</div>
  <dialog class="lightbox" id="lightbox">
    <img id="lightboxImg" alt="">
    <form method="dialog"><button type="submit">Close</button></form>
  </dialog>
</section>
"""


def about_main():
    return f"""
<article class="wrap page-hero">
  {crumbs([("About", None)])}
  <div class="split">
    <div class="prose">
      <p class="eyebrow">About the company</p>
      <h1>Owner-operated, based in Alma.</h1>
      <p class="lede">KS Lawn Ranger LLC is run by Kohlton. The phone number and email on this site reach the business directly. There is no published street address and no claim of a large crew — the work is quoted and carried out as an owner-operated company.</p>
      {actions("/contact/#quote")}
    </div>
    <div class="media">{picture("first-one", "Striped lawn maintained by KS Lawn Ranger", "(min-width: 980px) 42vw, 100vw", eager=True)}</div>
  </div>
</article>
<section class="section wrap prose">
  <h2>What the company actually does</h2>
  <p>The work covers the year. In the growing season that is weekly or bi-weekly mowing and edging, bed weeding, and shrub trimming. Spring and fall add leaf removal and haul-away. Install work includes mulch, decorative rock, sod, landscaping, and hardscaping such as patios and retaining walls. Fall is when aeration and overseeding are scheduled. Winter is snow removal and ice management for homes and for commercial properties, including a seasonal snow contract if you want to be on the route before the first storm.</p>
  <p>Mulching mowers are the standard finish. Bagging can be added to a quote. Core-aeration plugs are left on the lawn to break down. Snow service does not promise bare pavement, because refreeze, drifting, and traffic can put ice back on a surface after a visit.</p>
  <h2>How to hire the company</h2>
  <p>Estimates are free. Most of them start with the address and a look at the property, because lot size, obstacles, and haul-away change the job. You can call or text {PHONE_DISPLAY}, email {EMAIL}, or use the form. Say whether the property is a home or a business, and pick phone, text, or email as the way you want the reply.</p>
  <p>Hours are Monday through Saturday, 7:00 AM to 6:00 PM. Sunday is closed. Payment is cash, check, Venmo, or a QuickBooks payment link. Invoices are available on request, and estimates and billing are handled in QuickBooks. The company is fully insured, and proof is available on request.</p>
  <h2>Where the route runs</h2>
  <p>{esc(AREA_SENTENCE)}</p>
  <p>A portrait and a longer personal bio are not on this site yet. The photos in the <a href="/gallery/">gallery</a> are the record of the work. Questions that come up often are collected on a single <a href="/faq/">FAQ page</a>.</p>
</section>
"""


def faq_main():
    blocks = []
    for question, answer in FAQS:
        blocks.append(
            f"<details><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>"
        )
    return f"""
<article class="wrap page-hero prose">
  {crumbs([("FAQ", None)])}
  <p class="eyebrow">FAQ</p>
  <h1>One list of answers.</h1>
  <p class="lede">Pricing, timing, snow, insurance, and the towns on the route. If your question is not here, call or text {PHONE_DISPLAY}.</p>
</article>
<section class="section wrap faq">
  {''.join(blocks)}
</section>
"""


def contact_main():
    return f"""
<article class="wrap page-hero">
  {crumbs([("Contact", None)])}
  <p class="eyebrow">Contact</p>
  <h1>Call, text, or send the address.</h1>
  <p class="lede">The fastest quote starts with the property address and what you want done. Estimates are free.</p>
  <div class="grid-3" style="margin-top:1.25rem">
    <div class="plain-card"><h3>Phone and text</h3><p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a></p></div>
    <div class="plain-card"><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
    <div class="plain-card"><h3>Hours</h3><p>Monday–Saturday<br>7:00 AM – 6:00 PM<br>Sunday closed</p></div>
  </div>
</article>
<section class="section wrap">
  <h2>Service area</h2>
  <p>{esc(AREA_SENTENCE)}</p>
  {area_list()}
  <p>Based in Alma, Kansas. A street address is not published. Payment: cash, check, Venmo, and a QuickBooks payment link. Fully insured, proof on request.</p>
</section>
"""


def commercial_main():
    return f"""
<article class="wrap page-hero">
  {crumbs([("Commercial services", None)])}
  <div class="split">
    <div>
      <p class="eyebrow">Commercial</p>
      <h1>Lawn and snow service for businesses.</h1>
      <p class="lede">KS Lawn Ranger LLC maintains commercial properties as well as homes. A weekly mowing route, bed and shrub work, seasonal cleanup, and a snow contract can be quoted for the same site.</p>
      {actions()}
    </div>
    <div class="media">{picture("after-3-fixed", "Landscape bed after cleanup", "(min-width: 980px) 42vw, 100vw", eager=True)}</div>
  </div>
</article>
<section class="section wrap prose">
  <h2>What commercial service includes</h2>
  <p>The visit list is the same kind of work done at homes, scoped for a business property. That can be a weekly cut and edge along a storefront, bed weeding so planting areas stay defined, shrub trimming, a spring or fall cleanup with haul-away, or snow and ice work at entrances and other areas written into the quote.</p>
  <p>A weekly mowing route means the property is on a repeating schedule through the growing season instead of being called in when the grass is already tall. Bi-weekly is an option when growth is slower. Mulching is standard. Bagging is quoted when you want clippings removed. Hard surfaces that are part of the visit get blown off.</p>
  <h2>Snow contracts for businesses</h2>
  <p>A seasonal snow contract is for a business that wants to be on the route before the first storm, rather than shopping for help after the snow is already down. The quote names the surfaces — walks, entrances, and any other areas you want cleared — and whether ice melt is included per visit or as part of the plan. Pre-treatment can be requested when the weather allows.</p>
  <p>Bare pavement is not guaranteed. Refreeze, drifting, compaction, and traffic can make a surface slippery again after a visit. The job is to clear what is there at service time and open safe access. Details of timing are set in the quote. This site does not publish a response-time promise.</p>
  <h2>Insurance, invoices, and who to call</h2>
  <p>The company is fully insured, and proof is available on request — ask for it when you are comparing contractors for a commercial site. Invoices are available. Estimates and billing run through QuickBooks, and a QuickBooks payment link is one of the ways to pay, along with cash, check, and Venmo.</p>
  <p>Use the form and choose Commercial. Check “Weekly mowing route,” “Seasonal snow contract,” or both. Kohlton is the owner and the person behind {PHONE_DISPLAY}.</p>
  <p>{esc(AREA_SENTENCE)}</p>
  {related([
      ("Commercial snow removal", "/services/snow-removal-commercial/", "Entrances, agreed areas, and a contract set before winter."),
      ("Weekly mowing", "/services/lawn-mowing/", "Cuts, edging, and blow-off on a repeating route."),
      ("Bed maintenance", "/services/bed-maintenance/", "Weeding and edges so planting beds stay finished."),
  ])}
</section>
"""


SERVICES = {
    "lawn-mowing": dict(
        path="/services/lawn-mowing/",
        title="Weekly Lawn Mowing & Edging | KS Lawn Ranger",
        description="Weekly and bi-weekly lawn mowing, trimming, and edging for homes and businesses around Manhattan and Alma, KS. Free on-site estimates. Call (913) 221-7981.",
        h1="Weekly lawn mowing and edging.",
        eyebrow="Mowing",
        lede="A repeating cut, edges along the walks, and clippings blown off the concrete. Homes and businesses can both go on a route.",
        image="stripes",
        image_alt="Backyard with fresh mowing stripes",
        precheck="Weekly mowing route",
        service_name="Lawn mowing and edging",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Lawn mowing", None)],
        related=[
            ("Bed maintenance", "/services/bed-maintenance/", "Weeding and edges between mowing visits."),
            ("Aeration", "/services/aeration/", "Fall core aeration for lawns that are on the route."),
            ("Commercial mowing", "/commercial/", "The same cut, scheduled for a business property."),
        ],
        body="""
        <h2>What a mowing visit includes</h2>
        <p>A standard visit is the cut, trimming around fences, beds, posts, and tight spots, edging along sidewalks and driveways, and a blow-off of clippings from hard surfaces. The goal is a lawn that looks the same kind of finished every week, not scalped one visit and shaggy the next.</p>
        <p>Mulching is the standard finish. Clippings stay on the lawn and break down. If you want them bagged and removed, say so when you ask for a quote and it is priced with the rest of the visit. That is the only mowing option we spell out in advance, because bagging changes the time on site.</p>
        <h2>Weekly routes and bi-weekly cuts</h2>
        <p>The weekly mowing route is what most growing-season lawns need from the time grass takes off in spring until it slows in the fall. Bi-weekly is available when growth is slower or you do not need a cut every week. Check “Weekly mowing route” on the form if that is the schedule you want. The day is confirmed after the quote, not assigned by a call center.</p>
        <p>Cool-season lawns in this part of Kansas grow hard in spring and again in fall, and they coast more in the heat of midsummer. A route absorbs those fast weeks. Aeration and overseeding are not folded into a mowing stop. They are scheduled in the fall, usually September and October, when new seed has a chance. Leaf cleanup is also separate, so a heavy drop does not get chewed up and left in the beds.</p>
        <h2>How the quote is set</h2>
        <p>There is no price list on this site. Mowing quotes depend on lot size, obstacles, and how much trimming the property needs. Most residential prices are set after a quick on-site look. Text the address to {phone} if you want that look on the calendar. Tell us about dogs, locked gates, or anything that changes access so the visit is not a surprise.</p>
        <p>Businesses use the same form and choose Commercial. Invoices are available, and billing can go through QuickBooks. See the <a href="/commercial/">commercial services</a> page if the property is a storefront, office, or other business rather than a house.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "spring-fall-cleanup": dict(
        path="/services/spring-fall-cleanup/",
        title="Spring & Fall Cleanup in Manhattan, KS | KS Lawn Ranger",
        description="Spring yard cleanup and fall leaf removal with haul-away for Manhattan, Alma, Wamego, and nearby Kansas towns. Free estimates. (913) 221-7981.",
        h1="Spring and fall cleanup, with haul-away.",
        eyebrow="Seasonal cleanup",
        lede="Leaves, sticks, and bed debris come off the property. Spring resets the yard. Fall keeps the lawn from sitting under a wet mat of leaves.",
        image="leaves",
        image_alt="Pile of leaves collected at the curb for haul-away",
        precheck="Spring & fall cleanup / leaf removal",
        service_name="Spring and fall cleanup and leaf removal",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Spring and fall cleanup", None)],
        related=[
            ("Shrub trimming", "/services/shrub-trimming/", "Cutbacks that pair well with a spring cleanup."),
            ("Mulch and rock", "/services/mulch-rock/", "A refresh after the beds are cleaned out."),
            ("Weekly mowing", "/services/lawn-mowing/", "Start the route once the cleanup is done."),
        ],
        body="""
        <h2>Spring</h2>
        <p>A spring cleanup is the reset after winter. Leaves that packed into beds, sticks, and general lawn waste come out. Beds can be weeded and edged so the line between lawn and planting is visible again. Most properties around here schedule that work between March and May. The exact week depends on how early things green up, not on a fixed calendar date.</p>
        <p>Haul-away can be included. You should not be left with a pile at the curb unless that is what you asked for. If you want the cleanup to look finished rather than merely empty, mulch or rock and a shrub trim can be quoted with it. Those are separate services with their own pages, and they can share one visit when the quote says so.</p>
        <h2>Fall and leaf removal</h2>
        <p>Fall cleanup is mostly leaves, plus sticks that come down with them. Towns on this route have a lot of mature deciduous trees, especially Wamego and the older parts of Manhattan, and a single mowing pass will not deal with a real drop. Leaves are blown, piled, and hauled when haul-away is part of the quote. Doing that before the leaves mat down protects the turf you are paying to mow the rest of the year.</p>
        <p>Fall is also the right season to talk about <a href="/services/aeration/">aeration</a> and <a href="/services/overseeding/">overseeding</a>. Cleanup, aeration, and seed are coordinated so we are not seeding into a lawn still buried in leaves. If you only need leaves removed once, say that. If you expect more than one pass as trees finish dropping, say that too. The quote should match the number of visits.</p>
        <h2>What to send</h2>
        <p>The address, whether it is a home or a business, and a note about how heavy the leaves or beds are. Photos help, and an on-site look is still how most quotes are finished. Call or text {phone}. Check the cleanup box on the form, and add shrub trimming or mulch if you want them in the same estimate.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "landscaping": dict(
        path="/services/landscaping/",
        title="Landscaping Installs in Manhattan, KS | KS Lawn Ranger",
        description="Landscaping installs in the Manhattan and Alma area: beds, mulch, rock, sod, and plantings. Free on-site estimates from KS Lawn Ranger. (913) 221-7981.",
        h1="Landscaping installs, scoped on site.",
        eyebrow="Installs",
        lede="This is project work, not the weekly cut. Beds, mulch, rock, sod, and plantings are quoted as a job with a start and a finish.",
        image="mulch",
        image_alt="Installed mulch bed with plants and stepping stones",
        precheck="Landscaping install",
        service_name="Landscaping installation",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Landscaping installs", None)],
        related=[
            ("Mulch and rock", "/services/mulch-rock/", "The material and the edge, in detail."),
            ("Hardscaping", "/services/hardscaping/", "Patios and retaining walls when the project needs them."),
            ("Sod", "/services/sod/", "New turf where seed would take too long."),
        ],
        body="""
        <h2>Install work, not a maintenance visit</h2>
        <p>Weekly mowing keeps a lawn where it is. A landscaping install changes the yard: new or rebuilt beds, mulch or decorative rock, sod where the turf is gone, and plantings when you want something in the bed besides mulch. KS Lawn Ranger quotes that work on site. Tell us what you like — mulch or rock, a low-maintenance bed, a place where the lawn should stop — and the quote follows the property, not a package from a menu.</p>
        <p>Plant installs can be part of the same quote as prep and mulch. The existing service already includes that. We are not a landscape architecture office and we do not publish design fees or drawings. You get an on-site estimate, a clear scope, and the installation. Waste and old material are hauled when the quote includes haul-away.</p>
        <h2>How an install is usually sequenced</h2>
        <ul>
          <li>You send the address and a short description, or photos of the area.</li>
          <li>We look at access, the shape of the beds, and what has to come out.</li>
          <li>The quote names the work: edging, mulch or rock, sod, plants, and haul-away if you want it.</li>
          <li>The job is scheduled Monday through Saturday between 7:00 AM and 6:00 PM.</li>
        </ul>
        <p>Hardscaping — patios and retaining walls — is related and has its own page, because the labor and the materials are different from a bed of mulch. If the project needs both, one form submission is enough. Check landscaping and hardscaping.</p>
        <h2>After the install</h2>
        <p>New beds still need weeding. New sod needs water from you while it knits. If you want the lawn on a weekly route after the project, check that box too. Bed maintenance can follow an install so the edge we cut does not disappear by July. None of those follow-ups are assumed. They are on the quote if you ask for them.</p>
        <p>The company is fully insured, proof on request. Payment is cash, check, Venmo, or a QuickBooks payment link.</p>
        """,
    ),
    "hardscaping": dict(
        path="/services/hardscaping/",
        title="Patios & Retaining Walls | KS Lawn Ranger",
        description="Hardscaping in the Manhattan, Kansas area: patios and retaining walls, quoted on site by KS Lawn Ranger. Call or text (913) 221-7981.",
        h1="Patios and retaining walls.",
        eyebrow="Hardscaping",
        lede="Hardscaping here means patios and retaining walls, built to the scope in the quote. It is project work, looked at on site before a price is given.",
        image="hardscaping",
        image_alt="Paver patio next to river rock and a shed",
        precheck="Hardscaping",
        service_name="Hardscaping",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Hardscaping", None)],
        related=[
            ("Landscaping installs", "/services/landscaping/", "Beds and plantings that meet the new hardscape."),
            ("Mulch and rock", "/services/mulch-rock/", "Rock beds that often sit beside a patio or wall."),
            ("Gallery", "/gallery/", "Photos of patio, rock, and bed work."),
        ],
        body="""
        <h2>The two jobs this page covers</h2>
        <p>Patios and retaining walls are the hardscaping KS Lawn Ranger installs. A patio is the flat work: pavers or a similar surface where you actually sit or walk. A retaining wall holds a change in grade so a slope becomes a usable edge. Project photos on this site show a paver patio beside river rock, and a stone retaining wall with a rock bed finished in front of it. Those are the kinds of jobs this service refers to.</p>
        <p>Every site is different. Slope, access for materials, what is already in the ground, and how the patio has to meet a walk or a door all change the job. That is why there is no price on this page and no “starting at” number. The quote comes after an on-site look.</p>
        <h2>What to have ready</h2>
        <p>Send the address and say whether you are thinking about a patio, a wall, or both. Photos of the slope or the area you want paved help the first conversation. If other work belongs in the same project — a rock bed, mulch, or plants where the wall meets the yard — check landscaping on the form so it is one quote instead of two trips to talk about it.</p>
        <p>Old concrete, failed edging, and excavated soil are hauled away when haul-away is written into the quote. Do not assume a dumpster or disposal is included until you see it listed.</p>
        <h2>What this service is not</h2>
        <p>This is not an engineering stamp, a permit service, or a promise about drainage laws. If your city requires a permit for a wall or a patio, that is the property owner’s item to confirm. We build the hardscape described in the quote. Drainage is discussed on site when a slope is part of the reason for the wall, and the scope you approve is the scope that gets built.</p>
        <p>The company is fully insured, with proof on request. Work is scheduled Monday through Saturday, 7:00 AM to 6:00 PM. Call or text {phone}.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "mulch-rock": dict(
        path="/services/mulch-rock/",
        title="Mulch & Rock Installation | KS Lawn Ranger",
        description="Mulch and decorative rock installation for landscape beds around Manhattan, Alma, and Wamego, KS. Free estimates from KS Lawn Ranger. (913) 221-7981.",
        h1="Mulch and decorative rock.",
        eyebrow="Bed installs",
        lede="Beds are prepped, the edge is cut so the lawn stops where it should, and then mulch or rock goes down. Haul-away of the old material can be part of the quote.",
        image="after-2",
        image_alt="Shade bed after fresh mulch was installed around a tree",
        precheck="Mulch & rock install",
        service_name="Mulch and rock installation",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Mulch and rock", None)],
        related=[
            ("Bed maintenance", "/services/bed-maintenance/", "Weeding so a new mulch bed stays a bed."),
            ("Landscaping installs", "/services/landscaping/", "Plants and larger bed projects."),
            ("Spring cleanup", "/services/spring-fall-cleanup/", "Clean the beds out before the new mulch."),
        ],
        body="""
        <h2>Mulch, rock, or a mix</h2>
        <p>Mulch is the right finish for most planting beds: it covers soil, makes the bed read as finished, and is what you see in the darker bed photos on this site. Decorative rock is the better finish where you do not want organic material — along a side yard, around a downspout path, or in a bed you are tired of weeding every month. Some properties want both. The side-yard project in the gallery is a rock install against an existing stone wall. The foundation photo is mulch. Tell us which look you are after.</p>
        <p>The work is more than dumping material. Beds get prepped, the edge against the lawn is defined, and the mulch or rock is installed to the depth in the quote. A fuzzy edge is how a bed gets mowed into nothing by August. If you are already on a mowing route, the person edging the lawn and the person installing the bed should be working from the same line.</p>
        <h2>What the quote needs to say</h2>
        <p>How big the beds are, whether old mulch or weeds have to come out, and whether you want haul-away. Weed barrier is an option to discuss on site, not a default we hide in the job. Rock and mulch weigh different amounts and take different time, so they are not the same price. You will see that in the quote, not as a number published here.</p>
        <p>A fresh mulch bed is not a weed-free guarantee. Seeds still land in mulch. If you want the bed kept up after the install, add <a href="/services/bed-maintenance/">bed maintenance</a> to the same request. Spring is the busiest time for this work, often right after a <a href="/services/spring-fall-cleanup/">cleanup</a>. Fall is a good second window, once leaves are out of the beds and before winter.</p>
        <p>Fully insured, proof on request. Call or text {phone}, or check “Mulch &amp; rock install” on the form.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "sod": dict(
        path="/services/sod/",
        title="Sod Installation in Manhattan, KS | KS Lawn Ranger",
        description="Sod installation for new and repaired lawns around Manhattan, Alma, and Junction City, KS. Site prep and a free on-site estimate. (913) 221-7981.",
        h1="Sod installation for a lawn that has to exist now.",
        eyebrow="Sod",
        lede="Where seed would take the rest of the season, sod is laid on prepared ground. You handle the watering while it establishes. We handle the prep and the install.",
        image="sod",
        image_alt="Newly laid sod squares in a backyard",
        precheck="Sod installation",
        service_name="Sod installation",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Sod installation", None)],
        related=[
            ("Overseeding", "/services/overseeding/", "A better fit when the lawn is thin, not bare."),
            ("Landscaping installs", "/services/landscaping/", "Beds and edges that meet the new turf."),
            ("Weekly mowing", "/services/lawn-mowing/", "A route once the sod is ready to be cut."),
        ],
        body="""
        <h2>When sod is the right job</h2>
        <p>Sod is for ground that needs to be a lawn, not a thin lawn that needs more grass in it. Bare soil after a project, a worn-out area by a gate, or a new section of yard are the usual reasons. If the lawn is simply thin, <a href="/services/overseeding/">overseeding</a> after aeration is usually the better conversation, and it costs a different kind of visit. We will say so on site rather than sell sod you do not need.</p>
        <p>The install starts with prep. The surface has to be ready to receive sod: graded enough to meet walks and existing turf, and not full of the debris that would telegraph through the new grass. Sod is laid so the seams are tight. The photo on this page is a backyard install against a walk and a fence, which is the scale of many of these jobs — a defined area, not a guess at an entire farm.</p>
        <h2>Watering is part of success, and it is yours</h2>
        <p>New sod has to stay watered while the roots take. We give straightforward watering guidance for the timing of the install and the yard. We do not stay to run the hose all week, and a quote does not include a sprinkler system unless that was a separate discussion. If you cannot water, say that before the sod is scheduled. Sod laid and then left dry is a wasted job.</p>
        <p>In this climate the practical windows are spring and early fall, when the heat is less likely to cook a new lawn on the truck and on the ground. Midsummer installs can be done when the site requires it, and the watering burden is higher. The quote will match the season you are actually in.</p>
        <h2>After it is down</h2>
        <p>The first mowing waits until the sod has rooted enough to take a cut. When it is ready, it can join a weekly route like any other lawn. Tell us the address, about how large the bare area is, and whether you want beds or edging done in the same visit. Call or text {phone}.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "shrub-trimming": dict(
        path="/services/shrub-trimming/",
        title="Bush & Shrub Trimming | KS Lawn Ranger",
        description="Hedge and shrub trimming with optional haul-away around Manhattan, Wamego, and Alma, KS. Free estimates from KS Lawn Ranger. (913) 221-7981.",
        h1="Bush and shrub trimming.",
        eyebrow="Trimming",
        lede="Hedges and foundation shrubs get a clean shape, and the clippings can leave with us. Timing depends on the plant, not on a single month for every bush in Kansas.",
        image="after-4-fixed",
        image_alt="Foundation hedge after it was trimmed into a clean shape",
        precheck="Bush & shrub trimming",
        service_name="Bush and shrub trimming",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Shrub trimming", None)],
        related=[
            ("Bed maintenance", "/services/bed-maintenance/", "Weeds and edges under the shrubs."),
            ("Spring cleanup", "/services/spring-fall-cleanup/", "A natural time to combine cutbacks and haul-away."),
            ("Mulch and rock", "/services/mulch-rock/", "Refresh the bed once the shrubs are back in bounds."),
        ],
        body="""
        <h2>What gets trimmed</h2>
        <p>Foundation plantings, hedges, and individual shrubs that have outgrown the space or gone soft and uneven. The work is a proper trim: shape that fits the bed, cuts that do not leave a shrub torn up, and a property that looks intentional when we leave. The gallery shows a foundation hedge brought back to a tight line along the front of a house. That is the kind of result this service is for.</p>
        <p>Haul-away of clippings is available and can be included in the quote. If you would rather keep the debris, say so. Most people do not want a pile of branches in the driveway after they paid for trimming.</p>
        <h2>Timing</h2>
        <p>There is not one best week for every plant. Spring-flowering shrubs and summer-flowering shrubs are not pruned on the same logic if you care about blooms. When we look at the property we will say what should wait and what can be cut now. A lot of shaping and hedge work around Manhattan and the smaller towns is simply about size: the bush is in the walk, the window, or the gutter. That can be scheduled with a <a href="/services/spring-fall-cleanup/">spring cleanup</a> so the haul-away happens once.</p>
        <p>Trimming is not the same visit as weekly mowing, even though a mowing stop includes trimming grass around obstacles. Shrub work is quoted on its own because the time and the debris are different. If you want both, check both boxes.</p>
        <h2>Asking for the estimate</h2>
        <p>Tell us how many shrubs or how much hedge, or send photos. An on-site look is still how the quote is finished when the property is large or the plants are overgrown enough that photos hide the interior. Fully insured, proof on request. {phone}.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "bed-maintenance": dict(
        path="/services/bed-maintenance/",
        title="Bed Weeding & Maintenance | KS Lawn Ranger",
        description="Landscape bed weeding, edging, and maintenance for homes and businesses around Manhattan and Alma, KS. Free estimates. (913) 221-7981.",
        h1="Bed weeding and maintenance.",
        eyebrow="Beds",
        lede="Weeds come out, the edge against the lawn is recut, and the bed still looks like a bed a month later. One visit or a repeating schedule.",
        image="after-6",
        image_alt="Foundation bed after mulch, kept defined against the lawn",
        precheck="Bed weeding & maintenance",
        service_name="Bed weeding and maintenance",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Bed maintenance", None)],
        related=[
            ("Mulch and rock", "/services/mulch-rock/", "New material when weeding alone will not refresh the bed."),
            ("Shrub trimming", "/services/shrub-trimming/", "The plants above the mulch."),
            ("Commercial services", "/commercial/", "Storefront beds on a schedule."),
        ],
        body="""
        <h2>Maintenance, as opposed to a new install</h2>
        <p>Bed maintenance is the upkeep: weeds pulled, grass creeping in from the lawn cut back, and the edge redefined. It is what keeps a mulch or rock bed from turning into the before photo in the gallery — tall weeds, lost edges, and soil showing through. If the bed needs a full layer of new mulch or rock, that is the <a href="/services/mulch-rock/">install</a>. If it needs to be held where it is, this is the service.</p>
        <p>One cleanup visit is enough for some properties, especially in spring. Others, including storefront beds that are seen every day, want it on a schedule so the weeds never get a month’s head start. Say which you want. A commercial property can put bed maintenance next to a weekly mowing route and have both on the same account, with an invoice through QuickBooks if you need it.</p>
        <h2>What you should expect</h2>
        <p>Weeds that are pulled are removed, not left wilted on the mulch, when haul-away or cleanup is part of the quote. Edges are cut so the mower has a line to follow on the next visit. We do not promise a bed will never grow another weed. Seed blows in. The point of maintenance is that someone is scheduled to deal with it.</p>
        <p>If shrubs in the same bed are overgrown, add trimming to the request. Doing the weeds and leaving a hedge on the walk is an unfinished job, and it is easy to price together. Spring and early summer are when beds get away from people. Fall is the other time, after leaves are out and before winter covers what was missed.</p>
        <p>Send the address and roughly how many beds. Photos of the worst one are useful. Call or text {phone}. The company is fully insured, proof on request.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "aeration": dict(
        path="/services/aeration/",
        title="Lawn Aeration in Manhattan, KS | KS Lawn Ranger",
        description="Core aeration for Manhattan, Alma, and nearby Kansas lawns. Fall is the main season. Plugs stay on the lawn. Free estimates. (913) 221-7981.",
        h1="Core aeration for compacted lawns.",
        eyebrow="Aeration",
        lede="Plugs are pulled so air and water can reach the roots. Fall is the main season. The plugs stay on the lawn and break down on their own.",
        image="aeration",
        image_alt="Soil plugs left on a lawn after core aeration",
        precheck="Aeration",
        service_name="Lawn aeration",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Aeration", None)],
        related=[
            ("Overseeding", "/services/overseeding/", "Seed right after aeration so it lands in open soil."),
            ("Weekly mowing", "/services/lawn-mowing/", "The route that keeps the lawn you just opened up."),
            ("FAQ", "/faq/", "Timing and how often to aerate."),
        ],
        body="""
        <h2>What core aeration does</h2>
        <p>Core aeration pulls plugs of soil out of the lawn instead of poking holes and pressing the sides tighter. That matters on the heavier soils along the Kansas River valley and on any yard that has been walked, played on, or mowed for years. Less compaction means water can soak in instead of running off, and roots get air. The photo on this page is what the lawn looks like the day it is done: plugs scattered on top of the grass.</p>
        <p>Leave the plugs. They break down and put that soil back into the turf. Raking them off is extra work that throws away the point. They look rough for a short time. That is normal, and the next mowing starts to break them up.</p>
        <h2>When to do it here</h2>
        <p>Fall is the best window, typically September through October. Temperatures are easing off and there is usually more moisture than in August. Spring aeration is available when a lawn needs it, but fall is the visit we recommend first. Most lawns do well with one core aeration a year. Heavy clay or high-traffic lawns may benefit from a second visit. We will say which camp a yard is in when we see it, not from a form.</p>
        <p>The strongest follow-up is <a href="/services/overseeding/">overseeding</a> immediately after, so seed sits in the openings the machine just made. If you want both, check both boxes. They can be one appointment. Watering after seeding is on you. We will tell you what the lawn needs for the week after.</p>
        <h2>Scheduling</h2>
        <p>Aeration season fills up because everyone in town wants the same six weeks. Send the address early in the fall, or in late summer if you already know you want it. Mark sprinkler heads and invisible dog fences if you have them, and mention them on the form. The visit is separate from weekly mowing even if you are on a route. Call or text {phone}.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "overseeding": dict(
        path="/services/overseeding/",
        title="Lawn Overseeding in Manhattan, KS | KS Lawn Ranger",
        description="Fall overseeding for thin lawns around Manhattan, Wamego, and Alma, KS. Best after aeration. Watering guidance included. (913) 221-7981.",
        h1="Overseeding for thin lawns.",
        eyebrow="Overseeding",
        lede="Seed goes down where the turf is thin, patchy, or tired. Fall is the season that works. The lawn you water afterward is the lawn you get.",
        image="overseeding",
        image_alt="Close view of young grass blades in a lawn",
        precheck="Overseeding",
        service_name="Lawn overseeding",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Overseeding", None)],
        related=[
            ("Aeration", "/services/aeration/", "Do this first so seed reaches soil."),
            ("Sod", "/services/sod/", "When an area is bare, not just thin."),
            ("Weekly mowing", "/services/lawn-mowing/", "How the lawn is maintained once seed is up."),
        ],
        body="""
        <h2>What overseeding is for</h2>
        <p>Overseeding thickens a lawn that is still a lawn. Thin spots, a faded color, and turf that has given ground to weeds are the reasons to do it. Seed is spread so new grass fills those gaps. It is not magic and it is not sod. If a section is bare dirt, talk about <a href="/services/sod/">sod</a> instead. If the lawn is mostly intact and just tired, seed is the right tool.</p>
        <p>A thicker lawn also leaves less open ground for weeds. That is a side effect of density, not a weed-control guarantee and not a spray program. KS Lawn Ranger is not selling a chemical package on this page. The service is aeration when you want it, seed, and plain instructions for water.</p>
        <h2>Timing and the aeration pair</h2>
        <p>Fall, typically September through October, is the window. Cooler air and more dependable moisture give seed a chance before winter, and the lawn comes out of that stronger in spring. Seed on a hard, unopened lawn sits on top and feeds birds. <a href="/services/aeration/">Core aeration</a> first is the combination we recommend so seed-to-soil contact is real. Book them together.</p>
        <p>Most seed germinates in 7 to 21 days. The range is wide because weather, water, and the grass type all move it. You need to water. We give simple guidance based on the yard and the week it was seeded. Skipping water is the usual reason a fall seeding looks like nothing happened.</p>
        <h2>Mowing around a new seeding</h2>
        <p>If you are on a weekly route, the cutting height and the timing of the next visits matter while seed is up. Tell us you overseeded, or book the route and the seeding from the same form so it is one plan. Spring seeding is possible depending on the goal, and we will say if fall would have been the better wait. Call or text {phone} with the address.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "snow-removal": dict(
        path="/services/snow-removal/",
        title="Snow Removal in Manhattan, KS | KS Lawn Ranger",
        description="Residential and commercial snow removal and ice management around Manhattan, Alma, and Junction City, KS. Seasonal contracts available. (913) 221-7981.",
        h1="Snow removal and ice management.",
        eyebrow="Winter",
        lede="Homes and businesses. A single visit after a storm, or a seasonal contract so you are already on the route. Ice melt is available. Bare pavement is not promised.",
        image="snow-removal",
        image_alt="A residential driveway cleared after a snow",
        precheck="Snow removal & ice management",
        service_name="Snow removal and ice management",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Snow removal", None)],
        related=[
            ("Residential snow", "/services/snow-removal-residential/", "Driveways, walks, and steps at a home."),
            ("Commercial snow", "/services/snow-removal-commercial/", "Entrances and contracts for businesses."),
            ("Fall cleanup", "/services/spring-fall-cleanup/", "Get leaves off the property before they freeze in place."),
        ],
        body="""
        <h2>Two kinds of customers, two pages</h2>
        <p>Snow work splits for a reason. A house needs the driveway, the front walk, the steps, and a path to the mailbox. A business needs the entrance customers and employees actually use, often on a contract that was signed before the season so the property is not scrambling after the first inch. Both are available. Pick the page that matches the property if you want the detail:</p>
        <ul>
          <li><a href="/services/snow-removal-residential/">Residential snow removal</a></li>
          <li><a href="/services/snow-removal-commercial/">Commercial snow removal and seasonal contracts</a></li>
        </ul>
        <p>You can also stay on this page and send the form. Choose Residential or Commercial, and check “Seasonal snow contract” if you want the all-winter arrangement rather than a one-time clear.</p>
        <h2>What ice management means here</h2>
        <p>Clearing snow is half of it. Ice melt or salt can be added per visit or written into the plan. Pre-treatment — putting material down before a storm when the forecast supports it — is available by request. It is not automatic. Ask for it when you want it, and it goes in the quote.</p>
        <p>We do not guarantee bare pavement. Weather changes after we leave. Surfaces refreeze. Snow drifts back. Cars pack what is left into ice. The work is to clear what is present at the time of service and open safe access. Anyone who promises a bare, dry lot for the entire day after a Kansas storm is selling something this company does not sell.</p>
        <h2>Get on the list before the storm</h2>
        <p>The useful time to call is before you need the service. A seasonal plan lets us know the address, the surfaces, and whether you want ice melt, so the route is built with you on it. A per-visit request still works, and it is how some homes prefer to handle a light year. Either way, send the address now. Hours in season are still Monday through Saturday, 7:00 AM to 6:00 PM. Call or text {phone}. The company is fully insured, proof on request.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "snow-removal-residential": dict(
        path="/services/snow-removal-residential/",
        title="Residential Snow Removal | KS Lawn Ranger",
        description="Residential snow removal for driveways, walks, and steps in Manhattan, Alma, Wamego, and nearby towns. Seasonal or per visit. (913) 221-7981.",
        h1="Snow removal for your home.",
        eyebrow="Residential snow",
        lede="Driveways, front walks, steps, and the short path that makes a house usable after a storm. One visit at a time, or a seasonal plan.",
        image="snow-removal",
        image_alt="Cleared residential driveway with snow piled to the side",
        precheck="Seasonal snow contract",
        property_type="Residential",
        service_name="Residential snow removal",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Snow removal", "/services/snow-removal/"), ("Residential", None)],
        related=[
            ("Commercial snow", "/services/snow-removal-commercial/", "If this is a business, start here instead."),
            ("Snow overview", "/services/snow-removal/", "Ice melt, pre-treatment, and what is not guaranteed."),
            ("Fall cleanup", "/services/spring-fall-cleanup/", "Leaves off the walks before they freeze down."),
        ],
        body="""
        <h2>The surfaces that matter at a house</h2>
        <p>Residential snow removal is about getting a household in and out. That is the driveway, the sidewalk in front, the walk to the door, the steps, and often a path to a mailbox or a side door you actually use. It is not a blank check to clear every inch of a rural acreage. The quote names the surfaces. If a drive is steep, narrow, or shared, say so. Those details change how the visit goes and they are easier to hear before a storm than during one.</p>
        <p>The photo on this page is a house driveway opened up with snow piled to the side. That is the result people are asking for: a place to park and a way to the door. Ice can still be present. See the note on bare pavement below.</p>
        <h2>Per visit or a seasonal plan</h2>
        <p>Some homes only call after a storm that is bigger than they want to shovel. That is a per-visit clear, and it depends on the route having room that day. A seasonal plan means the address is already known, the surfaces are agreed, and you are not introducing the property in the middle of a snowfall. Check “Seasonal snow contract” if that is what you want. The form defaults this page toward a home. Switch it if we have the wrong property type.</p>
        <p>Ice melt or salt can be added to any visit or included every time. Pre-treatment is by request when the weather allows, not an automatic extra. Tell us if the household includes someone who needs the walk open early, and we will talk about where that property sits on the route. We will not invent a clock-time guarantee on the website.</p>
        <h2>Limits, in plain language</h2>
        <p>We do not guarantee bare pavement. Refreeze overnight, wind, and tires will put slick spots back. Service clears what is on the ground at the time we are there and opens access. If you need a different standard, it has to be a conversation, not an assumption.</p>
        <p>This service covers the six core towns: Manhattan, Alma, Wamego, St. George, Junction City, and Ogden. If you are in Westmoreland or Paxico, send the address and we will confirm. A business property should use the <a href="/services/snow-removal-commercial/">commercial snow</a> page so the contract and the invoice match. Call or text {phone}.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
    "snow-removal-commercial": dict(
        path="/services/snow-removal-commercial/",
        title="Commercial Snow Removal | KS Lawn Ranger",
        description="Commercial snow removal and seasonal contracts for businesses around Manhattan and Junction City, KS. Insured, with QuickBooks invoices. (913) 221-7981.",
        h1="Commercial snow removal and seasonal contracts.",
        eyebrow="Commercial snow",
        lede="Entrances, walks, and the other areas named in the quote. A seasonal contract puts the business on the route before the first storm. Invoices are available.",
        image="snow-removal",
        image_alt="Cleared pavement after residential-style snow removal, shown as an example of cleared surfaces",
        precheck="Seasonal snow contract",
        property_type="Commercial",
        service_name="Commercial snow removal",
        nav="/services/",
        crumbs=[("Services", "/services/"), ("Snow removal", "/services/snow-removal/"), ("Commercial", None)],
        related=[
            ("Commercial services", "/commercial/", "Mowing and bed work for the same property in summer."),
            ("Residential snow", "/services/snow-removal-residential/", "Driveways and walks at a house."),
            ("Snow overview", "/services/snow-removal/", "Ice melt and the bare-pavement limit."),
        ],
        body="""
        <h2>What a commercial snow visit is</h2>
        <p>A business does not need the whole lot treated like a front yard, and it does need the places people walk. The quote lists them: the entrance, the sidewalk along the storefront, steps, and any other area you want cleared. Parking areas can be part of the scope when that is what you ask for and the site can be serviced with the equipment the job actually requires. We do not describe a fleet we have not published, and we do not promise a specific machine. The on-site look decides whether the property is a fit.</p>
        <p>Seasonal contracts are the version most businesses actually want. You are on the route for the winter. The surfaces and the ice-melt plan are agreed before the season, and you are not making a new introduction after the snow has started. Per-visit work is still possible when the calendar allows. Check “Seasonal snow contract” on the form — this page selects Commercial for you, and you can change it if the property is a home.</p>
        <h2>Ice, invoices, and insurance</h2>
        <p>Ice melt or salt is either per visit or part of the contract. Pre-treatment is available by request when conditions allow. Bare pavement is not guaranteed on commercial sites any more than it is at a house. Refreeze, drifting, and traffic will change a lot after we leave. The obligation is the service described in the quote: clear what is present and open access.</p>
        <p>Commercial accounts can be invoiced. Estimates and billing are handled in QuickBooks, and payment can be cash, check, Venmo, or a QuickBooks payment link. The company is fully insured. Ask for proof when you are approving a vendor. That request is normal and we expect it.</p>
        <h2>Pair it with the rest of the year</h2>
        <p>The same property often needs a weekly mowing route and bed maintenance once the snow is gone. One conversation can cover winter and the growing season. Start with snow if winter is the deadline, and mention mowing in the message. Hours are Monday through Saturday, 7:00 AM to 6:00 PM. Call or text {phone}. Homeowners should use <a href="/services/snow-removal-residential/">residential snow removal</a> so we scope a driveway instead of a storefront.</p>
        """.format(phone=PHONE_DISPLAY),
    ),
}


CITIES = {
    "manhattan-ks": dict(
        name="Manhattan",
        title="Lawn Care in Manhattan, KS | KS Lawn Ranger",
        description="Lawn mowing, landscaping, leaf cleanup, and snow removal in Manhattan, Kansas. Owner-operated from Alma. Free estimates. Call (913) 221-7981.",
        image="first-one",
        image_alt="Striped lawn in front of a Manhattan-area home",
        h1="Lawn care in Manhattan, Kansas.",
        lede="Manhattan is the largest city on the route. Weekly mowing, installs, fall leaves, and snow are all booked from the same Alma-based company.",
        body="""
        <h2>A full-size city on a small company’s route</h2>
        <p>Manhattan is where most of the weekly stops are. It has older streets with mature trees, newer subdivisions, rentals that turn over, and commercial frontage that needs the sidewalk and the grass kept in the same week. KS Lawn Ranger is not based inside the city. Kohlton runs the company from Alma, which is a straight shot west, and Manhattan is a core stop rather than an occasional trip.</p>
        <p>That matters for scheduling. A weekly mowing route only works if the town is one you are already driving. Manhattan is. Bi-weekly is available when a lawn does not need a cut every week. Businesses that want the same predictability can use the <a href="/commercial/">commercial</a> page and ask for a route plus, in winter, a seasonal snow contract.</p>
        <h2>Lawns, shade, and the river valley</h2>
        <p>A lot of Manhattan lawns deal with shade from old street trees and with soil in the Kansas River valley that stays soft after a rain. Soft ground is a reason to look at a property before promising a mowing day, not a reason to rut a yard because the route says Tuesday. Fall leaf drop on those same shaded streets is heavy enough that it is its own service. <a href="/services/spring-fall-cleanup/">Leaf removal and haul-away</a> is separate from the weekly cut so the beds are not left full of shredded leaves.</p>
        <p>Thin turf under trees is the usual reason Manhattan customers ask about <a href="/services/aeration/">aeration</a> and <a href="/services/overseeding/">overseeding</a> in September and October. Bare areas after a project are a sod conversation. None of those are included in mowing unless the quote says so.</p>
        <h2>Winter in town</h2>
        <p>Manhattan gets the storms that shut down a weekday. Homes need drives and walks. Businesses need entrances. Both are available, and the commercial version should be set up before the season. Read <a href="/services/snow-removal/">snow removal</a> for the limit we do publish: no bare-pavement guarantee. Ice melt can be part of the visit.</p>
        <p>Kansas State University’s calendar is not our schedule, but move-in and move-out weeks do create cleanup and mowing requests at rentals. If that is your property, say so in the message and send the address. We do not claim a campus contract.</p>
        <p>Call or text {phone}, or send the form. Estimates are free and usually start with an on-site look.</p>
        """,
    ),
    "alma-ks": dict(
        name="Alma",
        title="Lawn Care in Alma, KS | KS Lawn Ranger",
        description="Alma’s owner-operated lawn care company. Mowing, landscaping, cleanup, and snow removal from KS Lawn Ranger LLC. Call or text (913) 221-7981.",
        image="stripes",
        image_alt="Mowed residential backyard",
        h1="Lawn care in Alma, where the company is based.",
        lede="KS Lawn Ranger LLC is an Alma company. The route starts here and runs east through Wamego and St. George to Manhattan, west-north to Junction City, and over to Ogden.",
        body="""
        <h2>Home base, not an afterthought</h2>
        <p>Alma is Wabaunsee County’s seat and the town the business is based in. Being local shows up in ordinary ways: the person you reach at {phone} is Kohlton, the owner, and an Alma lawn is not a favor squeezed in after a bigger city’s route. In-town lots, properties on the edge of the Flint Hills, and the greener ground along the Mill Creek valley are all part of the same service list. We do not run a reduced menu at home and a full menu in Manhattan.</p>
        <p>Wind and thinner hill ground make some Alma lawns harder to keep thick than a sheltered town lot. That is a reason to talk about fall <a href="/services/overseeding/">overseeding</a> and <a href="/services/aeration/">aeration</a>, and a reason a quote should see the yard instead of assuming every lot is the same rectangle. If the lawn is already in decent shape, a weekly or bi-weekly mowing route is the whole job.</p>
        <h2>The rest of the property</h2>
        <p>Beds, shrub trimming, mulch, and rock installs are the same services offered down the road in Wamego and Manhattan. Spring cleanup in Alma is typically March through May. Fall leaf work depends on the trees you actually have — some in-town yards are heavy, some hill properties are not. Haul-away is available and should be in the quote if you want the debris gone.</p>
        <p>Snow on a shaded Alma drive, or on a slope, is worth a seasonal plan if you do not want to shovel it. Residential details are on the <a href="/services/snow-removal-residential/">residential snow</a> page. The company does not guarantee bare pavement.</p>
        <h2>Nearby, and not the same thing</h2>
        <p>Paxico is close and is treated as a nearby area, not a core town. Westmoreland is the same. If you are in either place, send the address and we will say yes or no. Core stops are Manhattan, Alma, Wamego, St. George, Junction City, and Ogden.</p>
        <p>Payment is cash, check, Venmo, or a QuickBooks payment link. Fully insured, proof on request. Hours Monday through Saturday, 7:00 AM to 6:00 PM.</p>
        """,
    ),
    "wamego-ks": dict(
        name="Wamego",
        title="Lawn Care in Wamego, KS | KS Lawn Ranger",
        description="Mowing, leaf removal, and landscaping in Wamego, Kansas, on the route between Alma and Manhattan. Free estimates. (913) 221-7981.",
        image="stihl-leaves",
        image_alt="Leaves collected in a yard for haul-away",
        h1="Lawn care in Wamego, Kansas.",
        lede="Wamego sits on the Kansas River and on Highway 24, between Alma and Manhattan. It is a core town on the route, not a detour.",
        body="""
        <h2>On the road the route already drives</h2>
        <p>From Alma, Wamego is the next stop east before St. George and Manhattan. That geography is why a weekly mowing route works here. The drive is the same one the company makes anyway. In-town lawns, many of them on modest lots with older houses, are the typical mowing stop. Bi-weekly is available when you do not need every week.</p>
        <p>Commercial properties in town can be quoted the same way as a house, with the property type marked Commercial and an invoice through QuickBooks if you want one. Nothing about Wamego’s size changes the insurance: the company is fully insured, proof on request.</p>
        <h2>Trees and the fall</h2>
        <p>Wamego’s older blocks have the kind of canopy that makes October and November a leaf job, not a mowing job with a few leaves in it. <a href="/services/spring-fall-cleanup/">Fall cleanup and haul-away</a> is the service. If you know your street drops leaves in waves, ask for more than one pass and have that written down. Spring cleanups, March through May, are the other seasonal spike. Beds that get opened up in spring are the ones that look right for a <a href="/services/mulch-rock/">mulch refresh</a>.</p>
        <p>River-bottom ground can hold moisture. If a lawn stays soft, the mowing day should respect that. Say so when you book the look. We would rather move a visit than leave tracks because a route sheet said to mow.</p>
        <h2>Snow and the rest of the list</h2>
        <p>Residential snow removal covers drives and walks. A seasonal plan is the better setup if you want the address known before the first storm. The limit is the same one we publish everywhere: no guarantee of bare pavement. Ice melt can be included.</p>
        <p>Shrub trimming, bed weeding, sod, and aeration are all available in Wamego on the same terms as in Manhattan. Call or text {phone}. Paxico, to the west, is a nearby area — send the address if you are there. Wamego itself does not need that extra confirmation.</p>
        """,
    ),
    "st-george-ks": dict(
        name="St. George",
        title="Lawn Care in St. George, KS | KS Lawn Ranger",
        description="Lawn mowing, new-lawn care, and snow removal in St. George, Kansas. On the Alma-to-Manhattan route. Free estimates. (913) 221-7981.",
        image="sod",
        image_alt="New sod in a residential backyard",
        h1="Lawn care in St. George, Kansas.",
        lede="St. George is a small city on U.S. 24 between Wamego and Manhattan. It is on the core route because it is on that drive, not because it was added as an SEO page.",
        body="""
        <h2>A small town between two stops we already make</h2>
        <p>St. George does not need its own crew or a different price sheet. It needs to be on the list, and it is. The company is based in Alma, comes through Wamego, and continues to Manhattan. St. George is in the middle of that line. Weekly mowing, edging, and blow-off work the same way they do in the larger towns. If the lawn is new and growing fast, weekly is the right request. If it is a small established yard, bi-weekly may be enough. The on-site look is how that is decided.</p>
        <h2>Newer lawns</h2>
        <p>A lot of housing in St. George is newer than the older cores of Alma or Wamego. Newer lawns have their own problems: sod or seed that was never quite finished, edges between beds and grass that were never cut clean, and thin spots after the first hot summer. <a href="/services/sod/">Sod</a> is the fix when an area is actually bare. <a href="/services/overseeding/">Overseeding</a> after <a href="/services/aeration/">aeration</a> is the fix when the lawn is thin. Bed edging and a first <a href="/services/mulch-rock/">mulch or rock</a> install are how a new yard starts to look maintained instead of recently built.</p>
        <p>If you are in a new house and you want one quote for “make the outside presentable,” check the services that apply and say that in the message. We would rather combine them than send you three separate estimates that do not account for each other.</p>
        <h2>Leaves and snow, at a smaller scale</h2>
        <p>Leaf cleanup is real here and usually a lighter version of Wamego’s canopy problem, unless you have the large trees. Snow is drives, walks, and steps. A seasonal contract is optional and useful if you do not want to shovel. There is no bare-pavement guarantee.</p>
        <p>St. George is one of the six core cities, together with Manhattan, Alma, Wamego, Junction City, and Ogden. Call or text {phone}. Hours are Monday through Saturday, 7:00 AM to 6:00 PM.</p>
        """,
    ),
    "junction-city-ks": dict(
        name="Junction City",
        title="Lawn Care in Junction City, KS | KS Lawn Ranger",
        description="Residential and commercial lawn care and snow removal in Junction City, Kansas. Insured, with invoices. Free estimates. (913) 221-7981.",
        image="hardscaping",
        image_alt="Paver patio and rock bed on a residential property",
        h1="Lawn care in Junction City, Kansas.",
        lede="Junction City is a core town: homes and businesses, weekly mowing, and winter contracts. It is the western end of the route, in Geary County.",
        body="""
        <h2>A different town than Manhattan, on purpose</h2>
        <p>Junction City sits where the Smoky Hill and Republican rivers meet, next to Fort Riley. It is larger and more spread out than Wamego or St. George, and it has a real mix of houses and commercial property. KS Lawn Ranger serves it as one of six core cities. We do not claim a contract on Fort Riley, and we do not imply one. If your property is in town — a house, a rental, a storefront, an office — it can be quoted like any other stop.</p>
        <p>The drive from Alma is longer than the drive to Wamego, which is why Junction City is named explicitly instead of being folded into “and surrounding areas.” It is on the route. Send the address and the service, and the quote accounts for the property itself.</p>
        <h2>Homes, rentals, and businesses</h2>
        <p>Residential work is mowing and edging, bed maintenance, shrub trimming, seasonal cleanup with haul-away, and the install work — mulch, rock, sod, landscaping, patios, and walls — when a property needs more than a cut. Rentals are still residential. If you need a yard brought back between tenants, describe that in the message. It is a cleanup and a mowing quote, not a special package with a made-up name.</p>
        <p>Businesses should mark the form Commercial. A weekly mowing route keeps a property from being called only when the grass is embarrassing. Bed maintenance keeps the front planting from going wild between those cuts. Invoices are available and billing can run through QuickBooks. Proof of insurance is available on request, which is the normal ask from a commercial client.</p>
        <h2>Snow contracts</h2>
        <p>Junction City businesses that need walks and entrances open all winter should ask for a <a href="/services/snow-removal-commercial/">seasonal snow contract</a> before the season, not during the first storm. Homes use <a href="/services/snow-removal-residential/">residential snow removal</a>. Ice melt can be included. Bare pavement is not guaranteed, for the same weather reasons as everywhere else we work.</p>
        <p>Call or text {phone}. Monday through Saturday, 7:00 AM to 6:00 PM.</p>
        """,
    ),
    "ogden-ks": dict(
        name="Ogden",
        title="Lawn Care in Ogden, KS | KS Lawn Ranger",
        description="Lawn mowing, bed work, leaf cleanup, and snow removal in Ogden, Kansas, just west of Manhattan. Free estimates from KS Lawn Ranger. (913) 221-7981.",
        image="mulch",
        image_alt="Mulched landscaping bed against a house",
        h1="Lawn care in Ogden, Kansas.",
        lede="Ogden is the small city immediately west of Manhattan, in Riley County. It is part of the Manhattan side of the route, with the full service list.",
        body="""
        <h2>Close to Manhattan, listed on its own</h2>
        <p>Ogden is easy to treat as a neighborhood of Manhattan, and that would be sloppy. It is its own city, on the Kansas River just west of town, and it is one of the six places KS Lawn Ranger names as a core service area. Because it sits on the Manhattan side of the map, a mowing route that is already in town can include Ogden without a special trip from Alma. You do not need a different company for a smaller city next door.</p>
        <p>Lots are mostly residential. Some are older and shaded, and the ground near the river can hold moisture the way other valley lawns do. If the yard stays soft after rain, say so. We would rather schedule the cut for a drier day than leave ruts. Weekly and bi-weekly mowing, edging, and blow-off are the standing services. Mulching is standard. Bagging is available if you ask for it in the quote.</p>
        <h2>Beds, leaves, and new turf</h2>
        <p>Shaded Ogden yards collect leaves and grow thin turf under trees. <a href="/services/spring-fall-cleanup/">Fall leaf removal</a> with haul-away keeps that off the grass. <a href="/services/aeration/">Aeration</a> and <a href="/services/overseeding/">overseeding</a> in September and October are how thin areas get thicker. Bed weeding and a mulch or rock install are available when the foundation plantings need more than a mow. Sod is available when a section is bare rather than thin.</p>
        <h2>Snow on a short drive</h2>
        <p>Residential snow removal in Ogden is usually a driveway, a walk, and steps — the same scope as a Manhattan house. A seasonal plan is worthwhile if you want the address on the route before a storm. There is no bare-pavement guarantee. Ice melt can be part of the visit. If you run a business in Ogden, mark the form Commercial and look at <a href="/services/snow-removal-commercial/">commercial snow</a>.</p>
        <p>Ogden does not require the “send your address so we can confirm” step that Westmoreland and Paxico do. It is a core city. Call or text {phone}, Monday through Saturday, 7:00 AM to 6:00 PM. The company is fully insured, proof on request, and based in Alma.</p>
        """,
    ),
}


def city_main(slug, city):
    image = picture(city["image"], city["image_alt"], "(min-width: 980px) 42vw, 100vw", eager=True)
    others = []
    for name, href, _ in CORE_AREAS:
        if name == city["name"]:
            continue
        others.append(f'<a href="{esc(href)}">{esc(name)}</a>')
    body = city["body"].format(phone=PHONE_DISPLAY)
    return f"""
<article class="wrap page-hero">
  {crumbs([("Service area", "/#service-area"), (city["name"], None)])}
  <div class="split">
    <div>
      <p class="eyebrow">{esc(city["name"])}, Kansas</p>
      <h1>{city["h1"]}</h1>
      <p class="lede">{city["lede"]}</p>
      {actions()}
    </div>
    <div class="media">{image}</div>
  </div>
</article>
<section class="section wrap prose">
  {body}
  <h2>The full service area</h2>
  <p>{esc(AREA_SENTENCE)}</p>
  <p>Other core towns: {" · ".join(others)}.</p>
</section>
"""


def thank_you():
    page = {
        "path": "/thank-you.html",
        "title": "Thank You | KS Lawn Ranger",
        "description": "Your quote request was sent to KS Lawn Ranger LLC. We will follow up during business hours.",
        "robots": "noindex, nofollow",
        "form": False,
        "nav": "/contact/",
        "main": f"""
<article class="wrap page-hero prose">
  <p class="eyebrow">Quote request sent</p>
  <h1>Thank you. We have the request.</h1>
  <p class="lede">Kohlton will follow up by the contact method you chose. Hours are Monday through Saturday, 7:00 AM to 6:00 PM.</p>
  <div class="actions">
    <a class="btn btn-green" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
    <a class="btn btn-ghost" href="sms:{PHONE_TEL}">Text</a>
    <a class="btn btn-primary" href="/">Back to the homepage</a>
  </div>
  <p>If the request was urgent, call or text {PHONE_DISPLAY} directly. Email {EMAIL} also reaches the business.</p>
</article>
""",
    }
    return page


def not_found():
    return {
        "path": "/404.html",
        "title": "Page Not Found | KS Lawn Ranger",
        "description": "That page is not on the KS Lawn Ranger site. Call (913) 221-7981 for lawn care in the Manhattan, Kansas area.",
        "robots": "noindex, follow",
        "form": False,
        "main": f"""
<article class="wrap page-hero prose">
  <p class="eyebrow">404</p>
  <h1>That page is not here.</h1>
  <p class="lede">The link may be old. The company is still easy to reach.</p>
  <div class="actions">
    <a class="btn btn-green" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
    <a class="btn btn-ghost" href="sms:{PHONE_TEL}">Text</a>
    <a class="btn btn-primary" href="/contact/">Get a Free Quote</a>
  </div>
  <p><a href="/">Home</a> · <a href="/services/">Services</a> · <a href="/gallery/">Gallery</a> · <a href="/faq/">FAQ</a></p>
</article>
""",
    }


def build():
    pages = []

    pages.append({
        "path": "/",
        "title": "Lawn Care in Manhattan, KS | KS Lawn Ranger",
        "description": "Owner-operated lawn mowing, landscaping, seasonal cleanup, and snow removal for Manhattan, Alma, Wamego, St. George, Junction City, and Ogden. Free estimates. (913) 221-7981.",
        "image": largest_jpg("first-one"),
        "preload": "first-one",
        "nav": "/",
        "form": True,
        "precheck": None,
        "form_heading": "Tell us about the property",
        "main": home_main(),
    })

    pages.append({
        "path": "/services/",
        "title": "Lawn, Landscape & Snow Services | KS Lawn Ranger",
        "description": "Mowing, cleanup, landscaping, hardscaping, aeration, and snow removal from KS Lawn Ranger LLC in the Manhattan, Kansas area.",
        "nav": "/services/",
        "crumbs": [("Services", None)],
        "form": True,
        "main": services_index_main(),
    })

    for slug, copy in SERVICES.items():
        pages.append({
            "path": copy["path"],
            "title": copy["title"],
            "description": copy["description"],
            "image": largest_jpg(copy["image"]),
            "nav": "/services/",
            "crumbs": copy["crumbs"],
            "service_name": copy["service_name"],
            "form": True,
            "precheck": copy.get("precheck"),
            "property_type": copy.get("property_type"),
            "main": service_shell(copy),
        })

    pages.append({
        "path": "/commercial/",
        "title": "Commercial Lawn & Snow Service | KS Lawn Ranger",
        "description": "Commercial mowing routes, bed maintenance, and seasonal snow contracts around Manhattan and Junction City, KS. Insured. Invoices available. (913) 221-7981.",
        "image": largest_jpg("after-3-fixed"),
        "nav": "/commercial/",
        "crumbs": [("Commercial services", None)],
        "service_name": "Commercial lawn care and snow removal",
        "form": True,
        "property_type": "Commercial",
        "precheck": "Weekly mowing route",
        "main": commercial_main(),
    })

    for slug, city in CITIES.items():
        path = f"/areas/{slug}/"
        pages.append({
            "path": path,
            "title": city["title"],
            "description": city["description"],
            "image": largest_jpg(city["image"]),
            "nav": "/#service-area",
            "crumbs": [("Service area", "/#service-area"), (city["name"], None)],
            "form": True,
            "form_heading": f"Request a quote in {city['name']}",
            "main": city_main(slug, city),
        })

    pages.append({
        "path": "/gallery/",
        "title": "Project Gallery | KS Lawn Ranger",
        "description": "Before-and-after photos of mowing, mulch, rock, sod, shrub trimming, and snow removal by KS Lawn Ranger LLC.",
        "nav": "/gallery/",
        "crumbs": [("Gallery", None)],
        "form": True,
        "form_heading": "Want this kind of work at your property?",
        "main": gallery_main(),
    })

    pages.append({
        "path": "/about/",
        "title": "About KS Lawn Ranger | Owner-Operated in Alma",
        "description": "KS Lawn Ranger LLC is owner-operated by Kohlton and based in Alma, Kansas. Fully insured. Serving Manhattan and five nearby towns.",
        "image": largest_jpg("first-one"),
        "nav": "/about/",
        "crumbs": [("About", None)],
        "form": True,
        "main": about_main(),
    })

    pages.append({
        "path": "/faq/",
        "title": "Lawn Care FAQ | KS Lawn Ranger",
        "description": "Answers on mowing quotes, aeration timing, haul-away, snow limits, insurance, payment, and the KS Lawn Ranger service area.",
        "nav": "/faq/",
        "crumbs": [("FAQ", None)],
        "faq": True,
        "form": True,
        "main": faq_main(),
    })

    pages.append({
        "path": "/contact/",
        "title": "Contact KS Lawn Ranger | Free Quote",
        "description": "Call or text (913) 221-7981 or email kslawnranger@gmail.com. Monday–Saturday 7am–6pm. Free lawn and snow estimates.",
        "nav": "/contact/",
        "crumbs": [("Contact", None)],
        "form": True,
        "form_heading": "Send a quote request",
        "main": contact_main(),
    })

    pages.append(thank_you())
    pages.append(not_found())

    written = []
    for page in pages:
        written.append(write_page(page))

    redirects = [
        ("/lawn-mowing-manhattan-ks.html", "/services/lawn-mowing/", "Lawn mowing"),
        ("/spring-cleanup-manhattan-ks.html", "/services/spring-fall-cleanup/", "Spring and fall cleanup"),
        ("/landscaping-manhattan-ks.html", "/services/landscaping/", "Landscaping"),
        ("/snow-removal-manhattan-ks.html", "/services/snow-removal/", "Snow removal"),
        ("/bush-shrub-trimming-manhattan-ks.html", "/services/shrub-trimming/", "Shrub trimming"),
        ("/aeration-manhattan-ks.html", "/services/aeration/", "Aeration"),
        ("/overseeding-manhattan-ks.html", "/services/overseeding/", "Overseeding"),
    ]
    for old, new, label in redirects:
        redirect(old, new, label)

    urls = []
    for page in pages:
        if page["path"] in ("/thank-you.html", "/404.html"):
            continue
        if "noindex" in page.get("robots", ""):
            continue
        priority = "1.0" if page["path"] == "/" else "0.8"
        urls.append(
            f"""  <url>
    <loc>{ORIGIN}{page["path"]}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>{"weekly" if page["path"] == "/" else "monthly"}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap)
    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /thank-you.html\n"
        "\n"
        f"Sitemap: {ORIGIN}/sitemap.xml\n"
    )
    check_links()
    print(f"Wrote {len(written)} pages, {len(redirects)} redirects, sitemap {LASTMOD}")


def check_links():
    hrefs = re.compile(r'(?:href|src)="([^"]+)"')
    missing = []
    html_files = list(ROOT.rglob("*.html"))
    for path in html_files:
        if "preview-" in str(path) or "/originals/" in str(path):
            continue
        text = path.read_text(errors="ignore")
        for match in hrefs.findall(text):
            if match.startswith(("http://", "https://", "tel:", "sms:", "mailto:", "#", "data:")):
                continue
            target = match.split("#")[0]
            if not target:
                continue
            rel = target.lstrip("/")
            candidate = ROOT / rel
            if candidate.is_dir():
                candidate = candidate / "index.html"
            if not candidate.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {match}")
    if missing:
        print("BROKEN LINKS:")
        for item in missing:
            print(" ", item)
        raise SystemExit(1)
    print(f"Link check ok across {len(html_files)} html files")


if __name__ == "__main__":
    build()
