# CMS Assistant - Invoice Generator

A Python-based invoice generation system that processes Word document templates and integrates with Google Sheets for work item tracking.

## Features

- **Invoice Template Processing**: Replace placeholders in Word documents with current dates
- **Google Sheets Integration**: Read work items from Google Sheets for invoice generation
- **Automated Date Handling**: Support for TODAY, LAST_MONTH, and PAY_BY_DATE placeholders
- **Flexible Configuration**: JSON-based configuration files for different clients

## Project Structure

```
cms-assistant/
├── Invoice_Generator/
│   ├── configurations/
│   │   └── alpineai.json          # Client configuration files
│   ├── templates/
│   │   └── Invoice-ComplianceMadeSimple-AplineAI.[LAST_MONTH].[TODAY].docx
│   ├── invoice_generator.py       # Main invoice generation script
│   ├── google_doc_reader.py       # Google Sheets integration class
│   ├── test_google_reader.py      # Test script for Google Sheets
│   └── setup_oauth.py             # OAuth2 setup helper
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## Installation

1. **Clone the repository** (if applicable) or ensure you have all files in place

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets OAuth2 authentication** (see section below)

## Google Sheets OAuth2 Setup

Since service account keys are disabled in many GSuite organizations, this project uses OAuth2 authentication, which is more secure and organization-compliant.

### Step 1: Create OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **APIs & Services** > **Library**
4. Enable the following APIs:
   - **Google Sheets API**
   - **Google Drive API**
5. Go to **APIs & Services** > **Credentials**
6. Click **Create Credentials** > **OAuth client ID**
7. Choose **Desktop application**
8. Download the JSON file

### Step 2: Set Up Credentials

1. **Save the downloaded JSON file** in your project directory (e.g., `.vscode/` folder)
2. **Set the environment variable** in your `.vscode/common.env` file:
   ```bash
   GOOGLE_CREDENTIALS_PATH=.vscode/client_secret_YOUR_CLIENT_ID.apps.googleusercontent.com.json
   ```
   
   **Example:**
   ```bash
   GOOGLE_CREDENTIALS_PATH=.vscode/client_secret_1049835516666-5v9s988evv40904gof6p0i7l93f57go7.apps.googleusercontent.com.json
   ```

3. **Alternative: Use absolute path:**
   ```bash
   export GOOGLE_CREDENTIALS_PATH="/full/path/to/your/credentials.json"
   ```

### Step 3: Authenticate

The authentication will happen automatically when you first run the Google Sheets reader. The system will:

1. **Automatically detect your credentials file** from the environment variable
2. **Open a browser window** for Google authentication (first time only)
3. **Ask you to sign in** with your GSuite account
4. **Request permissions** to access Google Sheets
5. **Save authentication tokens** locally for future use

**Note:** The first run will require browser authentication. Subsequent runs will use the saved tokens automatically.

### Step 4: Test the Setup

1. **Set your Google Sheets URL** in your `.vscode/common.env` file:
   ```bash
   GOOGLE_DOC_LINK=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
   ```

2. **Test the connection:**
   ```bash
   python Invoice_Generator/test_google_reader.py
   ```

**Example configuration in `.vscode/common.env`:**
```bash
GOOGLE_DOC_LINK=https://docs.google.com/spreadsheets/d/1FBL5z0ZlK8Td7cnAF49O0y9L1cKnm3VjpGpSYkzFUaI/edit?usp=sharing
GOOGLE_CREDENTIALS_PATH=.vscode/client_secret_1049835516666-5v9s988evv40904gof6p0i7l93f57go7.apps.googleusercontent.com.json
```

## Usage

### Invoice Generation

1. **Create a configuration file** (see `configurations/alpineai.json` for example):
   ```json
   {
       "template": "Invoice_Generator/templates/Invoice-ComplianceMadeSimple-AplineAI.[LAST_MONTH].[TODAY].docx",
       "invoice_folder": "/path/to/your/invoice/folder/",
       "copy_invoice_PDF_to_folder": "/path/to/backup/folder"
   }
   ```

2. **Run the invoice generator:**
   ```bash
   python Invoice_Generator/invoice_generator.py configurations/alpineai.json
   ```

### Google Sheets Integration

The `GoogleDocReader` class can read work items from Google Sheets:

```python
from Invoice_Generator.google_doc_reader import GoogleDocReader
from datetime import date

# Initialize reader
reader = GoogleDocReader(
    url="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
    sheet_name="AlpineAI",
    target_month=date(2025, 1, 1)  # January 2025
)

# Connect and retrieve data
if reader.connect():
    work_items = reader.retrieve_work_items()
    reader.print_all_items()
    total_hours = reader.compute_total_hours()
    print(f"Total hours: {total_hours}")
```

## Configuration

### Invoice Generator Configuration

The configuration file should contain:

- **template**: Path to the Word document template
- **invoice_folder**: Base folder for generated invoices
- **copy_invoice_PDF_to_folder**: Backup folder for PDF copies

### Google Sheets Data Format

The Google Sheets should have the following columns:
- **Column A**: Date (various formats supported)
- **Column B**: Topic
- **Column C**: Working item description
- **Column D**: Hours worked

## Date Placeholders

The invoice generator supports these placeholders in templates:

- `[TODAY]` → Current date in "MMMM dd, YYYY" format (e.g., "January 15, 2025")
- `[LAST_MONTH]` → Previous month in "MMMM YYYY" format (e.g., "December 2024")
- `[PAY_BY_DATE]` → Current date + 30 days in "MMMM dd, YYYY" format

## Troubleshooting

### OAuth2 Authentication Issues

1. **Browser doesn't open**: Check your system's default browser settings
2. **Permission denied**: Ensure you're using your GSuite account
3. **Network issues**: Verify internet connection and firewall settings
4. **Credentials not found**: Check that `GOOGLE_CREDENTIALS_PATH` points to the correct file

### Common Solutions

1. **Verify environment variables:**
   ```bash
   # Check if environment variables are set correctly
   echo $GOOGLE_CREDENTIALS_PATH
   echo $GOOGLE_DOC_LINK
   ```

2. **Re-authenticate:**
   ```bash
   rm authorized_user.json  # Remove old tokens
   python Invoice_Generator/test_google_reader.py  # This will trigger re-authentication
   ```

3. **Check credentials file:**
   ```bash
   python Invoice_Generator/setup_credentials.py
   ```

4. **Verify Google Sheets access:**
   - Ensure the sheet is shared with your account
   - Check that the sheet name matches exactly
   - Verify the sheet has data in the expected format
   - Confirm the Google Sheets URL is correct

### Dependencies Issues

If you encounter import errors:

```bash
pip install --upgrade -r requirements.txt
```

## Security Notes

- **Never commit credentials files** to version control
- **Add `credentials.json` and `authorized_user.json`** to your `.gitignore`
- **OAuth2 tokens are stored locally** and automatically refresh
- **No service account keys required** - more secure for organizations

## Development

### Testing

Run the test suite:
```bash
python Invoice_Generator/test_google_reader.py
```

### Adding New Features

1. **New date placeholders**: Add to `invoice_generator.py`
2. **New Google Sheets columns**: Modify `google_doc_reader.py`
3. **New configuration options**: Update configuration schema

## License

This project is for internal use. Please ensure compliance with your organization's policies when using Google APIs.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Google Cloud Console setup
3. Ensure all dependencies are properly installed
4. Check that your GSuite account has the necessary permissions
