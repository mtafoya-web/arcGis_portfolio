# Project presentation audit and implementation plan

Audit date: October 30, 2026. Scope: local Python, Jinja templates, CSS, README, and `data/Geog 11 Projects .md`. The findings below describe the original application; see the implementation update for the changes made afterward.

## Latest image update from the data folder

All 11 published projects now use matching images from the owner's newly supplied files. The seven existing projects have updated or newly filled galleries; four additional projects from the Markdown now have pages because their images establish clear matches. Original files under `data/` are unchanged. Thirteen distinct images are used; duplicate Disneyland and coordinate-comparison views are omitted in favor of the clearer versions.

| Project | Selected source files |
| --- | --- |
| Disneyland energy conservation | `image3.png` (larger version of `image2.png`) |
| Orange County water quality | `image16.png` |
| Lower 48 population | `image10.png`, `image11.jpg`, `image8.png` |
| LA County crisis zones | `image6.png` |
| CSU campuses | `image12.png` |
| Mojave National Preserve | `image15.png` |
| Orange County population density | `image9.png` |
| Canada Lambert projection | `image4.jpg` |
| Congressional district comparison | `image5.png` |
| California coordinate systems | `image7.png` (closer view of the layout also in `image13.png`) |
| PCC reflection-pond digitization | `image14.jpg` |

The larger crisis-zone layout explicitly describes urban development and roads intersecting wildlife habitat. Its description and caption now reflect that topic instead of the hospital-location wording in the Markdown. New workflow screenshots are identified as such in their captions; no interactive capability is claimed for them. Disneyland remains the leading interactive showcase.

Several source files have mismatched PNG/JPEG extensions. Served copies use extensions matching their actual binary format, preserving the original pixels. Copies live under `static/images/projects/` so validation and static serving stay unchanged. No project uses an otter placeholder now; the otter still serves as the site's brand image. The original Markdown's unresolved hand-drawn map remains unpublished.

## Previous content and showcase update

The owner supplied a closer Disneyland embed and requested project images and editorial polish. This supersedes the earlier placeholder-only instruction for images with confirmed project matches.

- Updated Disneyland to the light theme, center `-117.92005139702917,33.81127780256998`, and scale `18055.954822`. Scroll zoom is disabled, matching its omission from the new embed. The other five supplied controls remain enabled.
- Edited the published titles, summaries, and descriptions for spelling, concise wording, correct terminology, and readable paragraphs. Population mapping now describes the actual city/state symbol methods instead of referring to countries. The Disneyland description distinguishes the Monorail route from point locations without treating a biodiesel railroad as zero-emission transportation.
- Extracted six original PNGs without altering their pixels: source images 1–3 are the Lower 48 population gallery, image 5 is Disneyland, image 6 is the newly added LA County crisis-zone project, and image 7 is Orange County water quality. Image 4 remains unassigned because its Oregon-area screenshot does not have a confirmed project match. The original Markdown is preserved.
- Added descriptive alt text and captions for every assigned image. CSU campuses, Mojave National Preserve, and Orange County population density keep placeholders because no matching images were supplied. Source images are modest-resolution originals; higher-resolution exports can replace them later.
- Featured interactive projects have a visible label and a direct map-section link. The detail flow is project summary and section links, interactive map, write-up, then map gallery. Static project cards and the three-image population gallery retain complete map layouts without cropping.
- All 12 automated tests pass; strict mypy reports no issues in eight source files, and the dependency check passes. No new packages were added.

Signed-out Chrome checks at 1440px and 390px confirmed the homepage, portfolio listing, and population gallery have no horizontal overflow and load no ArcGIS module. The Disneyland map opens in the supplied light theme and at the requested center and scale; its basemap and both operational layers load. An actual click on the mobile showcase button reaches the map-section anchor. The mobile action is 44px high, preview spacing was tightened, and gallery images retain their complete layouts. No JavaScript exceptions or failed network requests were observed during the initial browser pass.

Earlier sections below retain the original audit and prior implementation decisions for context.

## Implementation update: interactive maps supplied later

The owner will create and supply the interactive map embeds. Keep the existing otter images as placeholders until replacements are supplied; do not extract or substitute the Markdown images during this implementation.

- Implemented a shared, validated `data/projects.json` collection, the `/portfolio` listing, and `/portfolio/{slug}` detail pages. Homepage highlights and selected work use the same records. Six clearly described projects form the first batch; candidate projects needing clarification remain in the Markdown source.
- Every initial record uses `/static/images/otter_sprite.png`, identifies it as a placeholder, and sets `embed_url` to `null`.
- Each detail page supports one optional interactive map. Set `embed_url` to the `src` URL from the owner's iframe code, never the entire HTML snippet. The page creates the responsive, titled, lazy-loaded iframe and an external link. Without a URL, it shows the description and placeholder image without an empty iframe. Images remain available when an embed is present or fails to load.
- Approved exact hosts are declared in `app/models/projects.py`. Add an exact trusted hostname there if the owner uses a different ArcGIS organization or provider. URLs require HTTPS and reject credentials and custom ports.
- The first static image component doubles as the thumbnail, avoiding a redundant thumbnail field. Local image paths are validated under `static/images/`, allowing the existing otter placeholder; actual exports can later go under `static/images/projects/`.
- The About navigation link now targets the existing homepage section. The unfinished Resume link is omitted until its page is implemented.
- Added dependency manifests, strict mypy configuration, and focused tests for routes, template fields, empty content, optional embeds, escaped text, URL restrictions, duplicate slugs, and invalid image paths.

Remaining content work: supply embed URLs, verify each map works signed out and permits framing, replace placeholder images when desired, and clarify the remaining source projects. Restart the application after editing project JSON because content is loaded at startup.

Implementation verification: all seven automated tests pass, strict mypy reports no issues in eight source files, and `pip check` reports no broken requirements. Tests exercise the application through its ASGI test client; browser layout and real external embeds remain unverified. The original audit's dependency limitations below are historical and have been resolved locally.

## Disneyland ArcGIS component implementation

The owner supplied an ArcGIS script embed for the Disneyland energy conservation project. Implemented the following addition while preserving the existing placeholder images and iframe support:

- Added optional typed `arcgis_map` data, mutually exclusive with `embed_url`. It validates the 32-character hexadecimal item ID, longitude/latitude bounds, finite positive scale, light/dark theme, and explicitly approved HTTPS portal origin. Control flags map to individual boolean attributes; raw HTML is not accepted.
- Configured item `7997e897da4d472290638160c061c6b4` from `https://pcc-gis.maps.arcgis.com`, centered at `-117.92014749918334,33.85363966052069` with scale `144447.638572`, dark theme, and all six supplied controls enabled.
- The Disneyland detail page loads `https://js.arcgis.com/5.1/embeddable-components/` once through the template head block and renders the custom element at `width: 100%`, `height: 600px`, and `display: block`. Homepage previews, the listing, iframe projects, and image-only projects do not load this module.
- The existing interactive section contains the component and an external Map Viewer link; the placeholder gallery remains below it. No new packages or authentication flow were introduced.
- All 10 automated tests pass; strict mypy reports no issues in eight source files, and `pip check` reports no broken requirements. Tests cover the exact supplied attributes, script placement, disabled flags, validation, and compatibility with existing iframe behavior.

Use the ArcGIS script-embed instructions in the README for future maps. Restart the application after changing the data.

Signed-out browser verification passed in a fresh headless Chrome profile at desktop (1440px) and mobile (390px) widths. The Web Map and both operational layers loaded without credentials; desktop legend and mobile bookmarks opened, mouse-wheel zoom changed the map scale, and a real click opened the fallback Map Viewer link in a new tab. The map measured 1296x600px on desktop and 366x600px on mobile, with no horizontal overflow. The observed load produced no JavaScript exceptions or failed network requests. The local page, stylesheet, and placeholder image returned HTTP 200. Temporary verification screenshots and the test server were removed/stopped after inspection.

## Findings, in priority order

| Priority | Finding and evidence | Recommended action |
| --- | --- | --- |
| High | Every project button leads to `/portfolio`, but `main.py:17` defines only `/`. Navbar links to `/about` and `/resume` also have no matching routes (`templates/base.html:90`, `:98`, `:106`). | Implement the portfolio listing and project detail route together. Implement the other pages or remove their navigation links until ready. |
| High | Projects are disconnected from presentation. `User.projects` defaults to an empty list (`app/models/user.py:10`); initialization never populates it. Highlights are three duplicated blocks (`templates/index.html:57` onward); latest work loops over `range(6)` (`:170`). The separate ten-item `images` list is passed to the template but never used. Nothing reads `data/`. | Load one validated project collection and use it for all project sections. Adding the Markdown file alone currently changes nothing on the site. |
| High | The Markdown is an editorial source, not a consistent project dataset. It contains only three explicit `Project:` headings, approximately twelve candidate projects, seven base64 PNGs, and ambiguous image placement. | Curate a small structured dataset once. Do not build a parser that guesses project boundaries or image associations from paragraph order. |
| Medium | `Component.url` accepts any string (`app/models/component.py:6`), and the project model has no slug, preview image, summary, or dedicated embed field (`app/models/projects.py:4`). This is a readiness gap; no iframe is currently rendered. | Add only the fields required by the presentation described below. Validate external embed URLs separately from local image paths. |
| Medium | Project details in the grid are invisible until hover (`static/css/styles.css:339–359`). There is no equivalent keyboard-focus rule or touch-specific visible state. The grid remains two columns at all widths, with 220px-high items and 2rem overlay padding. | Keep titles and links visible on touch devices, reveal overlays on focus, and use a single column on small screens. Check long real project titles for clipping. |
| Medium | `object-fit: cover` crops grid images (`static/css/styles.css:329–336`). Cropping is acceptable for previews but would hide map legends, scales, and attribution in a detail view. | Show complete map layouts with `contain` or natural aspect ratio on detail pages, plus a link to the original image. |
| Medium | There is no dependency manifest, test suite, or static type-check configuration. Both the repository virtual environment and the default Python environment lack the app's dependencies. | Record runtime dependencies and use one Python type checker. Restore a working environment before claiming runtime or type-check success. |
| Low | `home()` has no return annotation (`main.py:18`), and the Jinja import has an unexplained `# type: ignore` (`:2`). Pydantic validates model construction, but it does not statically check Jinja field references. | Annotate the route as returning `HTMLResponse`; reassess the ignore after installing dependencies. Check rendered templates separately. |
| Low | Highlights advertise `Python · FastAPI · Bootstrap · GIS` for every project (`templates/index.html:69`, `:99`, `:129`). Those are site technologies, not evidence of each mapping project's tools. | Use only project-specific tools confirmed by the source. Choose featured items explicitly. |

## Where content and embeds should go

Keep the current FastAPI/Jinja/Bootstrap stack. No database, CMS, ArcGIS SDK, Markdown rendering engine, or frontend framework is needed for this portfolio.

| Surface | Content | Media and destination |
| --- | --- | --- |
| Home highlights | Up to three explicitly featured projects, each with title and one-sentence summary. | Preview image and link to `/portfolio/{slug}`. No live maps in the carousel. |
| Home latest work | Up to six projects from an explicitly curated order. Do not infer recency from source paragraph order or the year of a map's dataset. | Same project records and detail links; no second image collection. |
| `/portfolio` | All publishable projects, with title and short summary. A simple responsive grid is sufficient. | Static previews linking to the corresponding detail page. No filters or pagination initially. |
| `/portfolio/{slug}` | Title, summary, full description split into readable paragraphs, and course/tool/source notes when supplied. | Full map images with captions; an optional interactive-map section below the narrative; a visible external map link. Unknown slugs return 404. |

Use one detail template for every project. Keep long descriptions and interactive maps off the homepage. Do not generate separate templates for each assignment.

## Minimal data design

- Preserve `data/Geog 11 Projects .md` as the supplied source.
- Create `data/projects.json` as the small, curated runtime dataset. Load it once from a path anchored to the application directory, validate it with Pydantic, and assign the resulting projects to the existing user. Do not silently suppress malformed records.
- Extend `Project` with `slug`, `summary`, `featured: bool = False`, and `embed_url: HttpUrl | None = None`. Retain `title`, `desc`, and `components`; use the first static image component as the thumbnail. Require at least one component, using the current placeholder until real images are supplied.
- Keep `Component` simple: `name` is the image label/alt description, `url` is a local static-image path, and `desc` is a caption. Do not make the same field represent both images and iframes. Require a thumbnail to reference an existing image component, so it can reuse the image description.
- Require nonblank slugs, titles, summaries, and descriptions. Validate lowercase, hyphenated slugs and uniqueness across the collection. Check that image paths stay under `static/images/` and exist; retain the current placeholder path. Avoid a separate project ID when the slug is sufficient.
- Use JSON array order as the initial editorial display order. Add dates only when reliable project completion dates are supplied; dataset years are not project dates.
- Remove the unused placeholder `images` collection when templates start using the real projects. Keep profile data in its existing location for now.

JSON provides an explicit, reviewable handoff from the uneven Markdown without introducing a content-management system. Keep the current images for this implementation. If the owner later chooses to use the Markdown images, extract them to `static/images/projects/<slug>/` during content preparation, not on each request. Keep the supplied Markdown out of rendered HTML.

## Interactive-map handling

The supplied Markdown contains **zero iframe tags and zero ArcGIS/StoryMaps/app URLs**. Its only HTTP link is a Canvas submission download. Interactive content will require additional URLs from the owner.

- Store an optional embed URL as data, never a pasted iframe HTML snippet. Let the template create the iframe.
- For supplied URLs, require HTTPS and explicitly approved exact hosts. `HttpUrl` validates URL structure but does not establish provider trust, public access, or frame compatibility. Select the actual allowed hosts when the links arrive; do not use substring hostname checks.
- Render an iframe only on the relevant detail page, with a descriptive title, lazy loading, full-width responsive sizing, and enough height to operate the map on mobile. Avoid a short video-style aspect ratio for map controls.
- Show an external "Open interactive map" link alongside each iframe. If a supplied app cannot be framed, retain the link and a static preview. Do not add speculative sandbox restrictions that may break the app; test against the actual supplied provider.
- A missing embed URL simply omits the interactive section. A private or blocked app must still leave a useful page containing the description and static maps. Verify each URL signed out before publication.

## Source inventory and content gaps

The twelve rows below are candidate project groupings inferred from the prose, not twelve finalized records. Proposed labels need editorial confirmation where the source lacks a title.

| Candidate | Available material | Preparation needed |
| --- | --- | --- |
| CSU campuses across California | Explicit title and description, lines 1–2. | Supply a matching map image or link. |
| Mojave National Preserve | Explicit title and description, lines 4–5. | Supply a matching map image or link. |
| Lower 48 population mapping | Explicit title and description, lines 8–9; images 1–3 visually show graduated city symbols, dot density, and state population shading. | Group the three maps into one project. Confirm descriptions against the actual methods and differing data years shown in the maps. |
| Hand-drawn Los Angeles map | Canvas link and paragraph, lines 13–15. | Resolve "major cities" in the link label versus "parks" in the paragraph. Supply a public image; the Canvas link's accessibility was not verified. |
| Political-preference/census exercise | Paragraph, line 17. | Supply title and media; clarify the reference to 118th/119th feature classes and what change was measured. |
| Canada Lambert projection exercise | One sentence, line 19. | Confirm whether this is its own project or part of the coordinate-system exercise; supply goal, image, and any interactive URL. |
| LA/San Francisco coordinate systems | Paragraph, line 21. | Supply title and matching media. |
| Pasadena City College digitization | Paragraph, line 23. | Supply title and matching media. |
| LA County hospital/crisis mapping | Short paragraph, line 27; image 6 visibly titled "Crisis Zones in LA County 2026". | Confirm how the crisis map supports hospital siting before making stronger suitability claims. |
| Disneyland energy conservation | Detailed paragraph, line 28; image 5 visibly titled "Energy Conservation Features at Disneyland Resort". | Associate image 5 explicitly; it currently appears much earlier in the Markdown. |
| Orange County water quality | Detailed paragraph, line 31; image 7 visibly titled "Impaired Water Bodies in Orange County, California". | Associate image 7 explicitly and retain the 2024 assessment context. |
| Orange County population density | Detailed paragraph, line 33. | Supply matching media and preserve the 2020 census/classification notes. |

Image 4 is an ArcGIS Pro screenshot showing an Oregon-area map; its relationship to the listed projects is unconfirmed. Keep it unassigned until identified. The source uses image references before as well as after descriptions, so proximity alone is unreliable.

All seven PNG payloads decode successfully. They range from 617–624 pixels wide and 323–489 pixels tall. They are usable previews, but map labels are small; obtain higher-resolution exports when possible. Some images include editor UI or selection handles, which should be replaced by clean map exports before publication.

## Implementation order and acceptance checks

1. **Restore reproducible checks.** Record runtime dependencies, install them in the local environment, and configure one static type checker. Confirm app import and the existing homepage render. Annotate the route and resolve genuine type errors without broad ignores. Anchor template/static/data paths to the application directory so launch location does not change behavior.
2. **Curate a small first batch.** Populate the JSON with confirmed projects and the existing placeholder images, add the minimal model fields, and validate content and unique slugs at load time. Keep unresolved projects out of the published collection rather than inventing details.
3. **Build the portfolio journey.** Add the listing route and shared detail route/template, then replace homepage placeholder blocks with loops over the same records. Handle zero projects and zero featured projects gracefully; only show carousel controls when there is more than one slide. Resolve the remaining navigation links before release.
4. **Add supplied embeds.** Validate the real provider URLs and implement the optional iframe plus external-link fallback. Until URLs arrive, static map detail pages are complete and useful.
5. **Verify the actual content.** Check home, portfolio, a known detail page, and unknown-slug 404. Verify links reach the correct project, all static assets return successfully, paragraphs and map legends remain readable, keyboard/touch users can access project labels, and mobile maps are operable. Check empty content, a project without an embed, malformed content, and an embed that cannot load. Run the type checker and a dependency consistency check.

Keep automated coverage focused: route/template smoke checks and meaningful content-validation cases are sufficient for this size of site. Use a signed-out browser to verify public embeds; model validation cannot establish their availability.

## Verification performed during this audit

- Parsed all five Python source files with `ast.parse`: passed. This checks syntax, not imports or runtime behavior.
- Compared declared application GET routes against literal internal template links: `/about`, `/portfolio`, and `/resume` are unmatched. This is source inspection, not HTTP testing.
- Confirmed neither template references `user.projects`, and there is no Markdown loader or iframe renderer.
- Inspected all seven decoded source images and validated their base64 payloads and PNG dimensions. Temporary previews were removed from the workspace after inspection.
- Checked the repository virtual environment (Python 3.14.6) and default Python: FastAPI, Pydantic, Jinja2, email-validator, HTTPX, and static type checkers are missing. **Runtime rendering, HTTP behavior, and a static type-check pass remain unverified.** No dependencies were installed or changed for this audit.
- External links, public sharing permissions, CDN availability, and visual browser behavior were not tested. Those checks depend on a working runtime and the final supplied links.
