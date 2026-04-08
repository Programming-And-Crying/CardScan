# PRODUCT_SPEC.md

## 1. Product summary

Build a local-network web application for storing, searching, reviewing, and maintaining a business-card archive.

The system replaces a legacy archive that previously lived behind Evernote-related workflows and now exists as a historical database with scanned business cards and XML transcriptions.

The application must:
- run in a browser on desktop and mobile devices;
- authenticate users with login and password;
- support role-based and group-based access;
- keep **one contact with multiple business cards**;
- import historical data from the legacy source;
- support uploading a new card from desktop or phone browser;
- display the original scan and extracted data;
- support multilingual cards;
- preserve source data from XML and OCR;
- allow manual correction and human verification;
- keep comments and full change history.

---

## 2. Product goals

### 2.1 Primary goals
1. Centralize the archive of contacts and card scans.
2. Make cards discoverable by name, company, position, phone, email, and full text.
3. Preserve all original scans.
4. Allow office staff to upload and correct new cards.
5. Enforce access control by role and by group.
6. Preserve traceability: source of data, comments, audit log, history.

### 2.2 Success criteria for MVP
The MVP is successful when:
- users can sign in and search records they are allowed to see;
- admins can manage users and access groups;
- office managers can upload one new card at a time and edit records without deletion rights;
- users can open a contact page and see all linked cards;
- the system stores original scan, XML payload, OCR text, normalized fields, transliteration, comments, and change history;
- the system can import historical records through a pluggable import pipeline;
- there is a visible **Human Verified** flag on each card.

---

## 3. Core business rules

### 3.1 Main domain entity
The main entity is **Contact**.
A Contact can have **multiple Business Cards**.

### 3.2 Source priority
When building the final displayed data, the source priority is:
1. Manual edit
2. XML from historical source
3. OCR output

### 3.3 Visibility model
Visibility is controlled by:
- **Role**: what actions the user may perform;
- **Access Group membership**: which records the user may see.

A Contact may belong to one or more Access Groups.
All linked Business Cards inherit the Contact visibility for MVP.

### 3.4 Deletion
- Admin can delete contacts and cards.
- Office manager cannot delete contacts or cards.
- Read-only user cannot create, edit, or delete anything.

### 3.5 Versioning and history
Every important mutation must be recorded with:
- timestamp;
- user;
- object type;
- object id;
- action;
- field name;
- old value;
- new value.

### 3.6 Comments
Comments are required on:
- Contact;
- Business Card.

### 3.7 Human verification
Each Business Card has a boolean field **human_verified** and metadata:
- verified_by;
- verified_at.

### 3.8 Duplicate handling
MVP must **detect likely duplicates and show suggestions** on upload/edit flows, but must **not implement automatic merge**.
Manual merge is explicitly out of scope for MVP.

---

## 4. User roles

## 4.1 Admin
Permissions:
- full read access;
- full write access;
- delete contacts and cards;
- upload cards;
- import historical data;
- trigger reprocessing;
- manage users;
- manage roles;
- manage access groups;
- view logs, history, and failed processing tasks.

## 4.2 Office manager
Permissions:
- search and view allowed records;
- upload new cards;
- create contacts;
- edit contacts;
- edit card fields;
- attach a card to an existing contact;
- add and edit comments;
- mark card as Human Verified;
- view record history for allowed records.

Restrictions:
- cannot delete cards or contacts;
- cannot manage users/roles/system settings.

## 4.3 Read-only end user
Permissions:
- sign in;
- search within allowed scope;
- view contact pages and linked cards;
- view comments if record is visible.

Restrictions:
- cannot upload;
- cannot edit;
- cannot verify;
- cannot delete;
- cannot manage access.

---

## 5. Main user journeys

## 5.1 Search and view
1. User signs in.
2. User enters a query.
3. System returns matching contacts within the user's access scope.
4. User opens a Contact page.
5. User sees structured fields, comments, linked cards, card previews, card processing state, and history.
6. User opens a specific card and sees original image plus extracted data.

## 5.2 Upload a new card
1. Office manager signs in.
2. Opens upload page.
3. Selects a file or captures a photo from phone browser.
4. System stores the original file and creates a Business Card in status `uploaded`.
5. Background processing runs OCR, normalization, transliteration, and field extraction.
6. System suggests possible matching contacts.
7. Office manager chooses one of:
   - create a new Contact;
   - link to existing Contact;
   - save for later review.
8. Office manager reviews fields, edits if necessary, adds comments if needed, and optionally marks Human Verified.

## 5.3 Historical import
1. Admin prepares a legacy import configuration.
2. Admin runs import from the admin UI or management command.
3. Import pipeline reads records from an adapter.
4. System creates or updates Contacts and Cards.
5. XML is preserved as raw source.
6. OCR is run only when needed.
7. Import report is saved and visible to admin.

## 5.4 Manual correction
1. Admin or office manager opens a card.
2. Changes extracted fields.
3. System stores changed values with source `manual`.
4. Search index is refreshed.
5. Change history is appended.
6. User may mark the card Human Verified.

---

## 6. Required feature set

## 6.1 Authentication and authorization
The system must provide:
- login/password sign-in;
- session-based authentication for web UI;
- role-based permissions;
- group-based visibility restrictions;
- failed login protection;
- user activity audit.

## 6.2 Contact management
Each Contact must support:
- full name;
- first name;
- last name;
- middle name;
- alternative spellings;
- transliterated search forms;
- company;
- position;
- multiple phones;
- multiple emails;
- multiple websites;
- multiple addresses;
- notes;
- comments;
- access groups;
- linked business cards.

## 6.3 Business card management
Each Business Card must support:
- original file;
- generated thumbnail;
- source type;
- upload timestamp;
- processing status;
- OCR text;
- raw XML;
- OCR confidence;
- language or best-effort language detection output;
- needs_manual_review flag;
- human_verified flag and metadata;
- comments;
- history.

## 6.4 Upload
MVP upload requirements:
- one card at a time;
- desktop browser file upload;
- mobile browser file upload;
- mobile browser camera capture if supported by browser/device;
- file validation;
- progress/state feedback;
- post-upload review flow.

## 6.5 OCR and extraction
The system must:
- process image-based cards in background;
- store raw OCR text;
- extract best-effort structured fields;
- preserve OCR confidence if available;
- allow manual override of all extracted data.

## 6.6 XML handling
The system must:
- preserve raw XML exactly as source evidence;
- parse XML when compatible mapping exists;
- store parsed values with source `xml`;
- allow manual override.

## 6.7 Normalization and transliteration
The system must store at least three textual forms when possible:
- original text;
- normalized text;
- latinized/transliterated search text.

The product must **not attempt full translation** of cards in MVP.

## 6.8 Search
Search must support:
- full name;
- partial name;
- company;
- position;
- phone;
- email;
- OCR text;
- XML-derived text;
- transliterated text.

Search should rank results roughly by:
1. exact contact field matches;
2. strong partial matches in structured fields;
3. phone/email matches;
4. transliteration matches;
5. full-text matches in OCR/XML text.

## 6.9 Comments
The system must support threaded depth 1 only for MVP: plain comments attached to a Contact or Business Card.
Required fields:
- author;
- created_at;
- updated_at;
- text.

## 6.10 Change history
The system must store history for:
- Contact edits;
- Business Card edits;
- linking/unlinking cards to contacts;
- access group changes;
- Human Verified status changes;
- comment edits/deletes.

## 6.11 Review queue
The system must provide a queue or filter for cards that need review, including:
- low OCR confidence;
- missing key fields;
- newly uploaded cards not yet human verified;
- import exceptions.

## 6.12 Access groups
Admins must be able to:
- create groups;
- update groups;
- deactivate groups;
- assign users to groups;
- assign contacts to one or more groups.

---

## 7. Page list

The web application must have at least these pages:
- `/login`
- `/dashboard`
- `/contacts`
- `/contacts/<id>`
- `/cards/<id>`
- `/upload`
- `/review-queue`
- `/history/<entity>/<id>`
- `/admin/users`
- `/admin/groups`
- `/admin/imports`
- `/admin/tasks`
- `/admin/system`

The exact route names may differ if the framework requires it, but equivalent functionality is mandatory.

---

## 8. Data model requirements

## 8.1 Core entities
Mandatory entities:
- User
- Role
- AccessGroup
- Contact
- ContactAlias
- ContactPhone
- ContactEmail
- ContactWebsite
- ContactAddress
- BusinessCard
- ParsedField
- Comment
- ChangeHistory
- ProcessingTask
- ImportJob
- ImportJobRow

## 8.2 Search support
The system must maintain denormalized search fields on Contact and BusinessCard or an equivalent search document structure so that search is fast and predictable.

---

## 9. Non-functional requirements

## 9.1 Deployment
- local deployment only;
- no dependency on public cloud runtime;
- all files stored inside the local environment;
- OCR and search must run locally.

## 9.2 Device support
- modern desktop browsers;
- modern mobile browsers.

## 9.3 Reliability
- preserve originals;
- support backups of DB and media files;
- recover gracefully after worker failure;
- allow reprocessing failed cards.

## 9.4 Security
- hashed passwords;
- HTTPS in deployment profile;
- access control enforcement on every view and action;
- server-side validation;
- audit logs.

## 9.5 Scalability
The MVP target is around 1,000 historical cards, but the design must remain workable for at least tens of thousands of cards without redesign of the domain model.

---

## 10. Out of scope for MVP

Explicitly exclude from MVP:
- automatic duplicate merge;
- CRM integration;
- external contact sync;
- advanced tagging taxonomy;
- card archival workflow;
- analytics/reporting beyond basic admin views;
- multilingual translation of card text;
- native mobile apps.

---

## 11. Known blocker for full historical import

The exact historical importer **cannot be completed without the real legacy database schema and sample data**.

Therefore the implementation must deliver:
- a generic pluggable import framework;
- one fully working reference adapter against fixture data bundled in the repo;
- clear extension points for the real legacy adapter;
- documentation describing where to implement source-specific field mapping.

When the real schema is later added to the repo, Codex can implement the final adapter on top of that framework.
