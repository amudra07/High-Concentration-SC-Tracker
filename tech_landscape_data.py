"""
tech_landscape_data.py

Data for the SC Tech Tracker: high-concentration / large-volume
subcutaneous (SC) delivery platforms for monoclonal antibodies,
benchmarked against Dupixent and our internal (Daewoong) platforms.

Every competitor entry's `source_url` was confirmed against a live search
or fetch result during the original research pass (2026-07-07) and is
carried forward unchanged here. Where a number could not be confirmed,
`concentration_mgml` is left as None and `concentration_display` says so
explicitly rather than guessing. Internal entries (Hyperion, Thermicra)
have no external source since they are proprietary/unpublished.

`needle_size_g` is new: most competitors do not publicly disclose needle
gauge, so it is set to "Not disclosed" unless a source explicitly states
it. Confirm and fill in as real data becomes available.

Last updated: 2026-07-08 (Hyperion corrected 600 -> 700 mg/mL + 23G;
Thermicra split out as its own internal entry at 400 mg/mL + 18-20G).
"""

from datetime import date

LAST_UPDATED = date(2026, 7, 8)

PHASES = [
    "Proof-of-concept",
    "Platform PoC",
    "Preclinical",
    "Phase 1",
    "Phase 3",
    "Commercial",
    "CDMO service available",
    "Internal R&D",
]

CATEGORIES = [
    "Liquid + excipient",
    "Enzyme co-formulation",
    "Suspension / particle",
    "Crystalline",
]

CATEGORY_COLOR = {
    "Liquid + excipient": "#2a78d6",
    "Enzyme co-formulation": "#eda100",
    "Suspension / particle": "#199e70",
    "Crystalline": "#9085e9",
    "Internal": "#e34948",
}

ENTRIES = [
    {
        "id": "dupixent",
        "name": "Dupixent (reference product)",
        "developer": "Sanofi / Regeneron",
        "category": "Liquid + excipient",
        "phase": "Commercial",
        "concentration_mgml": 175,
        "concentration_display": "150\u2013175 mg/mL (300 mg/2 mL and 200 mg/1.14 mL presentations)",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Conventional liquid formulation with amino-acid/salt excipients.",
        "mechanism_long": (
            "Standard aqueous solution stabilized with L-arginine hydrochloride, "
            "L-histidine, polysorbate 80, sodium acetate and sucrose at pH ~5.9. "
            "No enzyme or particle technology \u2014 this is the incumbent liquid-"
            "formulation baseline every entry below is being compared against."
        ),
        "deals": [
            "Marketed since 2017 (atopic dermatitis) across 9 approved indications",
            "600 mg adult loading dose currently requires two separate 300 mg injections",
        ],
        "source_name": "FDA prescribing information (DailyMed)",
        "source_url": "https://fda.report/DailyMed/595f437d-2729-40bb-9c62-c8ece1f82780",
    },
    {
        "id": "alteogen",
        "name": "Hybrozyme / ALT-B4 (berahyaluronidase alfa)",
        "developer": "Alteogen",
        "category": "Enzyme co-formulation",
        "phase": "Commercial",
        "concentration_mgml": None,
        "concentration_display": "Not a concentration play \u2014 enables large-volume SC delivery. Precedent: Keytruda Qlex runs at 165 mg/mL.",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Recombinant hyaluronidase co-formulated with the mAb; temporarily clears the SC space for bulk fluid flow.",
        "mechanism_long": (
            "ALT-B4 temporarily hydrolyzes hyaluronan in the extracellular matrix, "
            "allowing larger injection volumes at essentially normal antibody "
            "concentrations rather than raising the intrinsic concentration itself. "
            "Same mechanism class as Halozyme's ENHANZE, and the subject of an "
            "active patent dispute between the two companies."
        ),
        "deals": [
            "Keytruda Qlex (MSD/Merck) \u2014 approved US Sep 2025, EU Nov 2025 \u2014 165 mg/mL precedent",
            "Sanofi/Regeneron \u2014 SC dupilumab, Phase 1 (NCT07646548, started Jun 2026); deal quietly running since 2019, disclosed Jun 2026",
            "Daiichi Sankyo \u2014 SC Enhertu (ADC), Nov 2024, up to $300M",
            "AstraZeneca \u2014 multiple oncology assets, Mar 2025, up to $1.35B",
            "Sandoz, Biogen, GSK/Tesaro (dostarlimab) \u2014 additional licenses",
        ],
        "source_name": "Pearce IP \u2014 Sanofi & Alteogen confirm SC dupilumab",
        "source_url": "https://www.pearceip.law/2026/06/18/sanofi-alteogen-confirm-development-of-subcutaneous-dupilumab/",
    },
    {
        "id": "enhanze",
        "name": "ENHANZE (rHuPH20)",
        "developer": "Halozyme",
        "category": "Enzyme co-formulation",
        "phase": "Commercial",
        "concentration_mgml": None,
        "concentration_display": "Not a concentration play \u2014 enables SC infusions up to ~600 mL",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Recombinant human hyaluronidase co-formulation; same mechanism class as ALT-B4.",
        "mechanism_long": (
            "rHuPH20 depolymerizes hyaluronan locally and transiently in the SC "
            "space, enabling bulk fluid flow and larger-volume SC injections/"
            "infusions of drugs that would otherwise need IV administration. "
            "Used in 10+ commercial products."
        ),
        "deals": [
            "Darzalex Faspro (daratumumab), Herceptin Hylecta (trastuzumab), Phesgo (pertuzumab/trastuzumab), Rituxan Hycela (rituximab), VYVGART Hytrulo",
            "Takeda \u2014 vedolizumab SC, licensed Jan 2026",
        ],
        "source_name": "Halozyme \u2014 ENHANZE technology overview",
        "source_url": "https://halozyme.com/drug-delivery-technologies/enhanze/solutions.php",
    },
    {
        "id": "hypercon",
        "name": "Hypercon (ex-Elektrofi)",
        "developer": "Halozyme",
        "category": "Suspension / particle",
        "phase": "Preclinical",
        "concentration_mgml": 500,
        "concentration_display": "Up to 500 mg/mL",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Solvent-based dehydration converts mAb solution into dense microparticles suspended in a non-aqueous vehicle.",
        "mechanism_long": (
            "Water is extracted from antibody-solution droplets, precipitating the "
            "protein into smooth, dense microparticles which are then suspended in "
            "a non-aqueous carrier. Removing water from the particle core, rather "
            "than diluting the protein in more liquid, is what allows concentration "
            "well beyond what a liquid formulation can hold. Demonstrated injectable "
            "in ~20 seconds at <20 N glide force through standard SC needles."
        ),
        "deals": [
            "Acquired by Halozyme, 2026, up to ~$900M",
            "Licensed to Vertex Pharmaceuticals, April 2026 \u2014 up to 3 drug targets, $15M upfront",
        ],
        "source_name": "Drug Delivery and Translational Research (2025)",
        "source_url": "https://link.springer.com/article/10.1007/s13346-025-01856-2",
    },
    {
        "id": "snapshot",
        "name": "SnapShot (glassy surfactant / MoNi)",
        "developer": "Surf Bio (Halozyme)",
        "category": "Suspension / particle",
        "phase": "Preclinical",
        "concentration_mgml": 600,
        "concentration_display": "600+ mg/mL \u2014 doses over 1,000 mg in a single standard autoinjector shot",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Spray-drying with a proprietary glassy polyacrylamide surfactant (MoNi) that keeps microparticle surfaces hard and non-tacky.",
        "mechanism_long": (
            "Commercial surfactants (e.g. Tween) depress the glass-transition "
            "temperature of spray-dried protein microparticles, leaving soft, "
            "tacky surfaces that stick together and clog injection. Surf Bio's "
            "MoNi surfactant enriches at the particle surface during drying and "
            "keeps it glassy above room temperature, yielding free-flowing, "
            "injectable ultra-high-concentration suspensions. This is the same "
            "underlying science published by the Stanford Appel lab (bioRxiv "
            "2024, peer-reviewed in Science Translational Medicine, Aug 2025) \u2014 "
            "SnapShot is that platform's commercial form, not a separate academic "
            "effort."
        ),
        "deals": [
            "Acquired by Halozyme, 2026, up to ~$400M",
            "No published in vivo data yet as of this research pass",
        ],
        "source_name": "Surf Bio (PRNewswire, Oct 2024) / Sci. Transl. Med. 2025",
        "source_url": "https://www.prnewswire.com/news-releases/surf-bio-to-highlight-potential-of-snapshot-platform-to-rapidly-deliver-ultra-high-concentration-mab-and-biologic-therapies-via-subcutaneous-injection-during-podd-2024-302283971.html",
    },
    {
        "id": "wuxihigh",
        "name": "WuXiHigh 2.0",
        "developer": "WuXi Biologics (CDMO)",
        "category": "Liquid + excipient",
        "phase": "CDMO service available",
        "concentration_mgml": 240,
        "concentration_display": "240 mg/mL achieved (vs. prior 200 mg/mL highest FDA-approved liquid mAb)",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "24+ proprietary viscosity-reducing excipient combinations plus high-throughput screening.",
        "mechanism_long": (
            "A formulation-development service (not a proprietary drug) offered "
            "to any biologics developer. Uses high-throughput viscosity/"
            "aggregation prediction and >24 proprietary excipient combinations "
            "to cut viscosity by up to 90% in liquid formulations. Increasingly "
            "layering in hyaluronidase co-formulation as an add-on option."
        ),
        "deals": ["Offered as a CDMO service \u2014 not tied to a specific drug developer"],
        "source_name": "WuXi Biologics",
        "source_url": "https://www.wuxibiologics.com/drug-product-development-services/",
    },
    {
        "id": "shicon",
        "name": "S-HiCon",
        "developer": "Samsung Biologics (CDMO)",
        "category": "Liquid + excipient",
        "phase": "CDMO service available",
        "concentration_mgml": 200,
        "concentration_display": ">200 mg/mL liquid formulations",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "pH/buffer/excipient optimization with an early 'Concentration Gate Check' feasibility screen.",
        "mechanism_long": (
            "A CDMO formulation-development service, launched Oct 2024. Screens "
            "pH, buffer species and excipients early to flag high-concentration "
            "feasibility risk before committing to full development, then "
            "optimizes to reduce viscosity and protein aggregation."
        ),
        "deals": ["Offered as a CDMO service \u2014 not tied to a specific drug developer"],
        "source_name": "Samsung Biologics (PRNewswire, Oct 2024)",
        "source_url": "https://www.prnewswire.com/news-releases/samsung-biologics-launches-high-concentration-formulation-platform-to-accelerate-high-dose-drug-development-302274810.html",
    },
    {
        "id": "crystalomics",
        "name": "Crystalomics",
        "developer": "Ajinomoto Althea (CDMO)",
        "category": "Crystalline",
        "phase": "CDMO service available",
        "concentration_mgml": 240,
        "concentration_display": "240 mg/mL increase over the soluble dosage form (infliximab model)",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Rapid (1-day) batch crystallization of full-length mAbs into a low-viscosity suspension.",
        "mechanism_long": (
            "Arranges antibody molecules into an ordered crystal lattice rather "
            "than keeping them dissolved, which lowers suspension viscosity at a "
            "given concentration versus the equivalent liquid. Althea's batch "
            "process completes crystallization in about a day versus weeks for "
            "older diffusion-based methods. This is the active commercial "
            "continuation of the same crystalline-mAb science first published by "
            "Genentech in 2003 (PNAS) \u2014 that original work never reached market "
            "on its own, but Crystalomics has: 4 of the top 10 pharma companies "
            "have signed development agreements."
        ),
        "deals": ["4 of the world's top-10 pharma companies under agreement (as of most recent disclosure)"],
        "source_name": "Crystalomics technical paper",
        "source_url": "https://generisgp.com/wp-content/uploads/2017/05/crystalomics-paper_lsc.pdf",
    },
    {
        "id": "zheng2026",
        "name": "Solvent-dehydration hydrogel microparticles",
        "developer": "MIT (Zheng et al., academic)",
        "category": "Suspension / particle",
        "phase": "Proof-of-concept",
        "concentration_mgml": 360,
        "concentration_display": "360 mg/mL (aqueous suspension)",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Continuous solvent-based dehydration precipitates antibody into hydrogel microparticles, resuspended in water.",
        "mechanism_long": (
            "Unlike the non-aqueous suspensions above, this platform keeps the "
            "final suspension aqueous while still reaching high concentration \u2014 "
            "the first aqueous formulation reported at concentrations comparable "
            "to non-aqueous ones. Glide force <20 N; structurally and functionally "
            "stable for 4 months post-processing in the published study. "
            "Earliest-stage entry on this list \u2014 academic proof-of-concept, no "
            "company or licensee yet identified."
        ),
        "deals": ["No commercial licensee identified as of this research pass"],
        "source_name": "Advanced Materials (2026)",
        "source_url": "https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202516429",
    },
    {
        "id": "hyperion",
        "name": "Hyperion",
        "developer": "Daewoong Pharmaceutical",
        "category": "Suspension / particle",
        "is_internal": True,
        "phase": "Internal R&D",
        "concentration_mgml": 700,
        "concentration_display": "700 mg/mL (IgG sample)",
        "needle_size_g": "23G",
        "mechanism_short": "Spray-drying with ethyl acetate to a powder form, resuspended in MCT oil as the injection vehicle.",
        "mechanism_long": (
            "The antibody solution is spray-dried using ethyl acetate as the "
            "drying solvent, converting it into a dense dry powder. The powder "
            "is then resuspended in medium-chain triglyceride (MCT) oil, a "
            "non-aqueous vehicle, immediately before injection. Removing water "
            "at the powder stage rather than diluting the protein in more "
            "liquid is what allows loading to 700 mg/mL while remaining "
            "injectable through a 23G needle."
        ),
        "deals": [],
        "source_name": "Internal data \u2014 Daewoong Pharmaceutical",
        "source_url": "",
    },
    {
        "id": "thermicra",
        "name": "Thermicra",
        "developer": "Daewoong Therapeutics",
        "category": "Suspension / particle",
        "is_internal": True,
        "phase": "Internal R&D",
        "concentration_mgml": 400,
        "concentration_display": "400 mg/mL",
        "needle_size_g": "18\u201320G",
        "mechanism_short": "Pressure-driven mold-milling process creates a homogeneous drug/carrier mix ahead of suspension.",
        "mechanism_long": (
            "Applies controlled pressure during a mold-milling step to blend "
            "the antibody into a homogeneous mixture with the carrier phase "
            "before final suspension, reaching 400 mg/mL through an 18\u201320G "
            "needle. Sister platform to Hyperion within Daewoong's internal SC "
            "delivery portfolio, using a distinct particle-formation route."
        ),
        "deals": [],
        "source_name": "Internal data \u2014 Daewoong Therapeutics",
        "source_url": "",
    },
    {
        "id": "lindy",
        "name": "Microglassification",
        "developer": "Lindy Biosciences",
        "category": "Suspension / particle",
        "phase": "Preclinical",
        "concentration_mgml": 400,
        "concentration_display": ">400 mg/mL",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Organic solvents rapidly (within seconds) strip water from protein solution to form spherical amorphous microbeads.",
        "mechanism_long": (
            "Produces dense, spherical, stable microbeads of the therapeutic "
            "protein through fast solvent-based water removal, then suspends "
            "them for SC injection. Originated at Duke University."
        ),
        "deals": ["Licensed to Novartis, Aug 2024 \u2014 $20M upfront, up to $934M milestones + royalties"],
        "source_name": "BusinessWire (Novartis deal)",
        "source_url": "https://www.businesswire.com/news/home/20240827920051/en/Lindy-Biosciences-Enters-Licensing-and-Collaboration-Agreement-With-Novartis-for-Multi-target-Drug-Delivery-Innovation",
    },
    {
        "id": "xeriject",
        "name": "XeriJect",
        "developer": "Xeris Biopharma",
        "category": "Suspension / particle",
        "phase": "Preclinical",
        "concentration_mgml": 432,
        "concentration_display": "432 mg/mL demonstrated (trastuzumab model); platform range ~400\u2013450 mg/mL",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Spray-dried particles resuspended in a non-aqueous, shear-thinning vehicle.",
        "mechanism_long": (
            "Ready-to-use, non-aqueous viscoelastic suspensions that shear-thin "
            "under injection force, easing syringeability despite very high "
            "loading. Compatible with standard prefilled syringes."
        ),
        "deals": [
            "Merck \u2014 option/collaboration, 2021, undisclosed mAbs",
            "Regeneron \u2014 research evaluation + option agreement, 2 undisclosed mAbs",
            "Horizon Therapeutics \u2014 teprotumumab (Tepezza) SC reformulation, 2022",
        ],
        "source_name": "Xeris Biopharma press releases",
        "source_url": "https://www.xerispharma.com/news-releases/news-release-details/xeris-biopharma-announces-research-collaboration-and-option",
    },
    {
        "id": "nanoform",
        "name": "Nanoforming",
        "developer": "Nanoform Biologics",
        "category": "Suspension / particle",
        "phase": "Preclinical",
        "concentration_mgml": 400,
        "concentration_display": "400+ mg/mL (some company materials state >500 mg/mL \u2014 treat as a range pending a single authoritative figure)",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Nebulization / controlled particle engineering into nanoparticles, avoiding hyaluronidase entirely.",
        "mechanism_long": (
            "Converts biologics into stable nanoparticles via a gentle, low-"
            "temperature process, minimizing degradation. Preclinical head-to-"
            "head data (Nanotrastuzumab) compared directly against Herceptin "
            "Hylecta \u2014 the ENHANZE-based commercial product \u2014 positioning "
            "Nanoform explicitly as a hyaluronidase-free alternative."
        ),
        "deals": [
            "Takeda \u2014 data presented at DDF Summit 2024",
            "First exclusivity agreement, May 2026, with a Nasdaq-listed US biopharma (>$1B market cap) \u2014 $1M initial fee, extendable, tens of millions in potential milestones",
        ],
        "source_name": "Nanoform (exclusivity agreement release)",
        "source_url": "https://www.nanoform.com/en/inside-information-nanoform-signs-first-exclusivity-agreement-for-ultra-high-concentration-subcutaneous-delivery/",
    },
    {
        "id": "ivl_biofluidic",
        "name": "IVL-BioFluidic",
        "developer": "Inventage Lab",
        "category": "Suspension / particle",
        "phase": "Platform PoC",
        "concentration_mgml": 400,
        "concentration_display": "400 mg/mL demonstrated (rituximab model, stable through a 25G needle); company also states a 750 mg per-injection dose target \u2014 kept separate since that figure is a dose target, not a confirmed mg/mL number",
        "needle_size_g": "25G",
        "mechanism_short": "Microfluidic particle-volume reduction; explicitly positioned as needing no hyaluronidase.",
        "mechanism_long": (
            "Converts antibodies into uniform microparticle formulations via "
            "microfluidics, reducing injection volume directly rather than via "
            "an enzyme co-formulation. CEO has explicitly framed this as a "
            "'next-generation' alternative to first-generation enzyme-based SC "
            "conversion."
        ),
        "deals": [
            "Raised \u20a998.5B for SC formulation platform development",
            "In technology-evaluation discussions with J&J, Roche, AstraZeneca, Gilead, Boehringer Ingelheim, Takeda",
        ],
        "source_name": "The Bio (Korean trade press)",
        "source_url": "https://www.thebionews.net/news/articleView.html?idxno=22646",
    },
    {
        "id": "celltrion",
        "name": "Celltrion SC platform",
        "developer": "Celltrion",
        "category": "Liquid + excipient",
        "phase": "Commercial",
        "concentration_mgml": 120,
        "concentration_display": "120 mg/mL \u2014 marketed Remsima SC/Zymfentra is a plain liquid formulation, NOT hyaluronidase-based",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Two generations: today's marketed product is conventional liquid; a newer internalized hyaluronidase platform is for future pipeline only.",
        "mechanism_long": (
            "Remsima SC (infliximab, marketed as Zymfentra in the US) is a "
            "120 mg/mL plain liquid formulation \u2014 the world's first SC "
            "infliximab, launched 2020 (EU) / 2024 (US). Separately, Celltrion "
            "announced in Dec 2025 that it has internalized hyaluronidase-based "
            "SC formulation technology for future products, starting with "
            "Herzuma SC (CT-P6 SC, trastuzumab biosimilar), currently in trials "
            "and being benchmarked against Herceptin Hylecta. Don't conflate the "
            "two \u2014 they're different formulation generations."
        ),
        "deals": [
            "Remsima SC / Zymfentra \u2014 commercial since 2020 (EU), 2024 (US)",
            "Herzuma SC (CT-P6 SC) \u2014 Phase 1, hyaluronidase-based, vs. Herceptin Hylecta",
        ],
        "source_name": "Pearce IP / clinicaltrials.gov protocol",
        "source_url": "https://www.pearceip.law/2025/12/08/celltrion-to-expand-use-of-sc-formulation-technology-including-to-develop-sc-trastuzumab-biosimilar/",
    },
    {
        "id": "regeneron_note",
        "name": "Regeneron (platform-shopping note)",
        "developer": "Regeneron",
        "category": "Enzyme co-formulation",
        "phase": "Preclinical",
        "concentration_mgml": None,
        "concentration_display": "N/A \u2014 not an independent platform",
        "needle_size_g": "Not disclosed",
        "mechanism_short": "Regeneron is a customer of two different external platforms, not a platform owner.",
        "mechanism_long": (
            "Worth tracking as a signal, not a technology: Regeneron is "
            "evaluating XeriJect (Xeris) for 2 undisclosed mAbs, in parallel "
            "with the long-running Alteogen ALT-B4 program for SC dupilumab. "
            "That suggests Regeneron isn't committed to one vendor and is "
            "hedging across mechanisms (particle suspension vs. enzyme)."
        ),
        "deals": ["Xeris \u2014 research evaluation + option agreement, 2 undisclosed mAbs"],
        "source_name": "Xeris Biopharma (Regeneron collaboration release)",
        "source_url": "https://xerispharma.gcs-web.com/news-releases/news-release-details/xeris-biopharma-announces-research-evaluation-collaboration-and",
    },
]


CATEGORY_META = {
    "Enzyme co-formulation": {
        "number": 1,
        "title": "Enzyme-assisted large-volume delivery",
        "subtitle": "Halozyme ENHANZE, Alteogen ALT-B4",
    },
    "Suspension / particle": {
        "number": 2,
        "title": "Non-aqueous particle / suspension",
        "subtitle": "Elektrofi, Surf Bio, Xeriject, Hyperion, Thermicra",
    },
    "Crystalline": {
        "number": 3,
        "title": "Crystalline suspensions",
        "subtitle": "Largely proof-of-concept, unlaunched",
    },
    "Liquid + excipient": {
        "number": 4,
        "title": "Conventional liquid + excipients",
        "subtitle": "Dupixent's current category",
    },
}


def get_entry(entry_id: str):
    for e in ENTRIES:
        if e["id"] == entry_id:
            return e
    return None


def entries_with_concentration():
    """Entries with a real, comparable mg/mL number \u2014 for the positioning chart."""
    return [e for e in ENTRIES if e["concentration_mgml"] is not None]


def entries_by_category(category: str):
    return [e for e in ENTRIES if e["category"] == category]
