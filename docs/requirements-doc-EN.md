# DocCreator App with Web Service and Key Generation

## 1. Overview
The DocCreator App is a system consisting of a desktop application, a verification web service, and a key generation script. It allows filling out Word templates, converting them to PDFs, digital signing, and optional upload to Nextcloud and public verification of whether the file is genuine and intact.

## 2. Components

### 2.1 Desktop Application

#### 2.1.1 Configuration
- Read main configuration from `config.ini`
- Configurable settings:
  - Path to template directory
  - Path to directory for author (signer) data
  - Path to public key file for PDF signature
  - Path to private key file for PDF signature
  - Archive (optional)
    - Nextcloud credentials
    - Upload setting (true/false)
    - Filename pattern for upload (Default: TemplateName-YYYY-MM-DD-ZZZ-ClientName-Signer.pdf)

#### 2.1.2 Template Management
- Read Word templates (.docx) from the configured template directory
- For each template, there is an associated .ini file with:
  - Document language
  - Variables with corresponding questions to be inserted into the Word template.

#### 2.1.3 Author Management (Signer)
- Creation of an author (signer) with the following information:
  - Full Name {{SignerFullName}}
  - Short Name {{SignerShortName}}
  - Email Address {{SignerEmail}}
  - Phone Number {{SignerPhone}}
  - Mobile Phone Number {{SignerMobilePhone}}
  - Role {{SignerRole}}
  - ExtraInfo1 {{SignerExtraInfo1}}
  - ExtraInfo2 {{SignerExtraInfo2}}
  - ExtraInfo3 {{SignerExtraInfo3}}
  - ExtraInfo4 {{SignerExtraInfo4}}
  - ExtraInfo5 {{SignerExtraInfo5}}
  - Signature Password
- Upload of a PNG file as signature
- Verification that the PNG file has a transparent background; rejection if transparent background is missing
- Encryption of the signature PNG with the provided password
- Saving author information in `Signer-ShortName.ini` in the configured directory
- Saving the encrypted signature as `Signer-ShortName-Signature.png` in the configured directory
- Deletion of an author and their data after entering the correct password (verification if the encrypted PNG file with signature can be decrypted and a valid PNG file is created. If not, the data is not deleted and an error message is displayed.)

#### 2.1.4 PDF Creation and Signing
- Filling out the selected Word template with user inputs
- Creating a fingerprint string of the document, available as {{Fingerprint}}
- Replacing the variable {{VerificationURL}} in the Word template with the URL for PDF verification
- Replacing the variable {{SignerSignature}} in the Word template with the decrypted signature PNG
- Replacing the variable {{CurrentDate}} in the Word template with the current date. The format is specified in the template .ini file with "current_date = DD.MM.YYYY" as standard. Use the known placeholders for this.
- Replacing all signer-related variables ({{SignerFullName}}, {{SignerShortName}}, etc.) with the corresponding values
- Converting the filled Word document to PDF (without Word installation)
- Digital signing of the PDF with the public key

#### 2.1.5 PDF Integrity Check
- Verification if the uploaded PDF was modified after signing
- Verification if the uploaded PDF was created with our system

#### 2.1.6 Nextcloud Integration (optional)
- Upload of the signed PDF to Nextcloud, if activated in config.ini
- Use of the configured filename pattern
- This serves as an electronic archive

#### 2.1.7 Logging
- Implementation of logging with levels DEBUG, INFO, WARNING, ERROR
- Output to log file and standard output
- DEBUG: Output of all variables
- INFO: Output of individual processing steps
- WARNING and ERROR for corresponding situations

#### 2.1.8 Form Data Storage
- Option to save the content of the form with the name of the form
- New menu item "Continue editing previous document" when saved data exists
- When an old document was saved, there is also the menu item "Delete data from previous document", which deletes the temporary files of the previous form.

### 2.2 Web Service for PDF Verification
- Python script that delivers an HTML file (configured as .thtml in config.ini) when called without POST data. This HTML file should contain a prompt for PDF upload to verify the integrity and signature of the PDF document.
- Processing of PDF upload and performing verification
- Configuration of the path to the private key in config.ini
- Strict checking of all inputs for possible misuse
- Return of the verification result to the web user
- Display of verification results:
  - Clear, easily understandable display of the result (e.g., "Verification successful" or "Verification failed")
  - For successful verification: Display of relevant document information (e.g., creation date, author)
  - For failed verification: Display of possible reasons for the failure
- Maintaining a separate log file for the web service:
  - Logging of all content-relevant information: date, time, document name, verification result
  - Configurability of the log path in config.ini
- Security note: The web service does not store the uploaded PDF file at any time. This must be clearly communicated on the HTML page.

### 2.3 Key Generation Script
- Generation of asymmetric key pairs for PDF signature
- Storage of the public and private keys at the location specified in config.ini

## 3. User Interface of the Desktop Application

### 3.1 Main Menu
- Document (leads to author (signer) and template selection and form)
- Author (leads to author (signer) creation, editing, deletion)
- Continue editing previous document (only if saved data exists)
- Delete data from previous document (only if saved data exists)

### 3.2 Document
- Dropdown menu for author (signer) selection
- Dropdown menu for template selection
- Dynamically generated input fields based on the selected template
- Password prompt for signature decryption
- Signature verification (decryption of PNG)
- Option to save the document, e.g., if the password was incorrect
- Button "Create and sign PDF"
- Dialog for saving the created PDF

### 3.3 Author
- Dropdown menu for selecting the author (signer) to edit or delete
- Button for creating a new author (signer)
- When selecting an author (signer), changes are only saved when the correct password is entered
- When selecting to delete an author (signer), deletion only occurs when the correct password is entered.

### 3.3 Dialogs
- Dialog for creating, modifying, and deleting an author (signer)
- Confirmation dialogs for important actions

## 4. Desktop App Workflow
1. Display main menu
2. If "Document" is selected: Proceed to author selection, template selection, and form
3. If "Author": Dialog for creation, editing, and deletion of all author data and signature upload, checking for transparent background
5. If "Continue editing previous document": Load saved temporary form data
6. If "Delete data from previous document": Delete saved temporary form data
7. If "Exit": close the program

## 5. Security
- Encryption of signature PNG: Only the correct password decrypts the file to a valid PNG
- Use of asymmetric encryption for PDF signature
- Secure handling of the private key for PDF signature
- Checking all inputs in the web service for possible misuse

## 6. Extensibility
- Modular structure for easy extension with additional functions
- Possibility to implement additional cloud storage integrations

## 7. Technical Requirements
- Development in Python
- Use of PyQt5 for the desktop application
- Use of docx2pdf or similar library for Word-to-PDF conversion without Word installation
- Implementation of the web service with a Python web framework (e.g., Flask)
- Use of secure cryptography libraries for encryption and signing

### 8. Deliverables
- Desktop application (executable file or Python script with dependencies)
- Web service for PDF verification (Python script)
- Key generation script
- Documentation for installation and usage (README.md)
- Example configuration files (config.ini, template ini)
- Changelog file to document changes and version history

## 9. Testing Requirements
- Unit tests for critical functions (encryption, signing, PDF generation)
- Integration tests for the entire workflow
- Security tests, especially for the web service

## 10. Maintenance and Support
- Regular updates to fix security vulnerabilities
- Documentation for future extensions and modifications

### 11. Future
- add multilanguage capabilities
