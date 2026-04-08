# ACCEPTANCE_CRITERIA.md

## 1. Setup and run

1. A developer can start the full stack from a fresh clone using documented steps.
2. The repository provides working commands for init, run, test, lint, and sample import.
3. The app runs fully inside a local environment without cloud dependencies.

---

## 2. Authentication

1. A user can sign in with login and password.
2. An unauthenticated user trying to open a protected page is redirected to the login page.
3. A signed-in user can sign out.
4. Failed login attempts are rejected gracefully.

---

## 3. Role permissions

### 3.1 Admin
1. Admin can view all contacts and cards.
2. Admin can create, edit, and delete contacts and cards.
3. Admin can manage users and groups.
4. Admin can access import and task admin pages.

### 3.2 Office manager
1. Office manager can view allowed contacts and cards.
2. Office manager can create and edit contacts.
3. Office manager can upload cards.
4. Office manager can edit card-derived fields.
5. Office manager cannot delete contacts or cards.
6. Office manager can add/edit comments.
7. Office manager can mark a card as Human Verified.

### 3.3 Read-only user
1. Read-only user can search and view allowed records.
2. Read-only user cannot access create/edit/delete actions.
3. Read-only user cannot upload or verify cards.

---

## 4. Access groups

1. A Contact can belong to multiple Access Groups.
2. A non-admin user sees a Contact only if at least one of the user's groups matches one of the Contact's groups.
3. A Contact detail page and linked card pages are inaccessible when the user lacks group access.
4. Search results exclude inaccessible records.

---

## 5. Contact pages

1. The contacts list page shows only visible records.
2. A contact detail page shows:
   - main fields
   - aliases
   - phones
   - emails
   - company
   - position
   - notes
   - comments
   - linked cards
   - access groups
   - history
3. A contact can have multiple linked cards visible on its page.

---

## 6. Business card pages

1. A card detail page shows:
   - original image
   - thumbnail or preview
   - processing status
   - OCR text if available
   - raw XML if available
   - extracted/normalized fields
   - source provenance where implemented
   - comments
   - Human Verified state
2. A card can be linked to an existing contact or a new contact.

---

## 7. Upload flow

1. Office manager can upload one card image from desktop browser.
2. Office manager can upload one card image from mobile browser.
3. The upload form supports camera capture input on compatible mobile browsers.
4. After upload, the system stores the original file and creates a Business Card record.
5. The uploaded card enters processing/review flow.

---

## 8. OCR and extraction

1. OCR processing runs asynchronously.
2. The system stores raw OCR text after successful OCR.
3. The system stores language detection output if produced.
4. The system extracts best-effort structured values.
5. Manual edits are preserved and are not overwritten by reprocessing.
6. Failed OCR is surfaced in processing status and review/admin pages.

---

## 9. XML handling

1. Raw XML is stored with the card when import provides it.
2. Parsed XML-derived fields can populate contact/card values.
3. XML-derived values remain traceable to source where the model supports provenance.

---

## 10. Search

1. Search finds contacts by exact full name.
2. Search finds contacts by partial name.
3. Search finds contacts by company.
4. Search finds contacts by position.
5. Search finds contacts by phone.
6. Search finds contacts by email.
7. Search can match OCR/XML text.
8. Search can match transliterated text.
9. Search results are filtered by access rights.
10. Structured exact matches rank above weak raw-text matches.

---

## 11. Comments

1. Admin and office manager can add comments to a Contact.
2. Admin and office manager can add comments to a Business Card.
3. Read-only users can view comments on visible records.
4. Comment edits are tracked in history or comment metadata.

---

## 12. History and audit

1. Editing a Contact creates history entries.
2. Editing a Business Card creates history entries.
3. Linking a card to a contact creates history entries.
4. Changing Human Verified creates history entries.
5. Changing access groups creates history entries.
6. The system stores actor and timestamp for each history row.

---

## 13. Human Verified flow

1. Admin can mark and unmark Human Verified.
2. Office manager can mark and unmark Human Verified.
3. Read-only users cannot change this flag.
4. The card detail page visibly shows Human Verified state.
5. Review queue can filter by Human Verified state.

---

## 14. Review queue

1. There is a page or operational view for cards needing review.
2. Cards can appear in the review queue because:
   - OCR failed
   - OCR confidence is low
   - key fields are missing
   - card is not Human Verified
3. Office manager can work through this queue.

---

## 15. Import framework

1. The repository contains a generic import framework.
2. The repository contains one working sample adapter backed by fixture data.
3. Running the sample import creates contacts and cards in the application.
4. Import results are recorded in ImportJob and ImportJobRow or equivalent models.
5. The code clearly separates generic import logic from source-specific adapter logic.

---

## 16. Documentation

1. README explains setup and run.
2. Docs explain environment variables.
3. Docs explain media storage and local deployment.
4. Docs explain how to add the real legacy adapter once schema samples are available.
5. Docs explain user roles and permissions.
