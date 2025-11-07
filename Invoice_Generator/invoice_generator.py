#!/usr/bin/env python3
"""
Invoice Generator Script
Processes invoice template Word documents by replacing placeholders with current dates.
"""

import os
import sys
import json
import argparse
from datetime import date, datetime
import calendar
from word_document_editor import WordDocumentEditor
from google_doc_reader import GoogleDocReader


def create_invoice_folder(invoice_folder_base, last_month_date):
    """Create folder with format YYYY-MM-DD <last month name> <last month year>"""
    folder_name = f"{last_month_date.strftime('%Y-%m-%d')} {last_month_date.strftime('%B %Y')}"
    folder_path = os.path.join(invoice_folder_base, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")
    
    return folder_path

def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)

def process_google_sheets_data(editor, config):
    """
    Process Google Sheets data and add working items to the Word document.
    
    Args:
        editor (WordDocumentEditor): The Word document editor instance
        config (dict): Configuration dictionary
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
    # Get Google Sheets configuration
    google_doc_link = os.getenv('GOOGLE_DOC_LINK')
    sheet_name = config.get('GSheet')
    
    if not google_doc_link:
        print("Error: GOOGLE_DOC_LINK environment variable not set")
        print("Google Sheets integration is required for invoice generation")
        sys.exit(1)
    
    if not sheet_name:
        print("Error: 'GSheet' not found in config file")
        print("Google Sheets integration is required for invoice generation")
        sys.exit(1)
    
    print(f"\nProcessing Google Sheets data...")
    print(f"Google Sheet: {google_doc_link}")
    print(f"Sheet name: {sheet_name}")
    
    try:
        # Check for custom period configuration
        period_from_str = config.get('period_from')
        period_to_str = config.get('period_to')
        
        if period_from_str and period_to_str:
            # Custom period specified
            print("Custom period specified in config")
            try:
                period_from = WordDocumentEditor.validate_date_format(period_from_str)
                period_to = WordDocumentEditor.validate_date_format(period_to_str)
                
                # Validate that period_from is before period_to
                if period_from > period_to:
                    print(f"Error: period_from ({period_from_str}) must be before period_to ({period_to_str})")
                    sys.exit(1)

                # If same year-month and period_to is the first (or equal to from), extend to last day of that month
                if period_from.year == period_to.year and period_from.month == period_to.month:
                    last_day = calendar.monthrange(period_from.year, period_from.month)[1]
                    period_to = period_to.replace(day=last_day)
                
                print(f"Looking for work items from: {period_from.strftime('%Y-%m-%d')} to {period_to.strftime('%Y-%m-%d')}")
                
                # Create GoogleDocReader instance with custom period
                reader = GoogleDocReader(google_doc_link, sheet_name, period_from.date(), period_to.date())
                
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            # Default behavior: use previous month
            last_month_date = WordDocumentEditor.get_last_month_date()
            target_month = date(last_month_date.year, last_month_date.month, 1)
            # Compute last day of that month
            last_day = calendar.monthrange(target_month.year, target_month.month)[1]
            period_from = target_month
            period_to = date(target_month.year, target_month.month, last_day)
            
            print(f"Target month: {target_month.strftime('%B %Y')}")
            print(f"Looking for work items from: {period_from.strftime('%Y-%m-%d')} to {period_to.strftime('%Y-%m-%d')}")
            
            # Create GoogleDocReader instance with single month
            reader = GoogleDocReader(google_doc_link, sheet_name, period_from, period_to)
        
        # Connect to the sheet
        print("Connecting to Google Sheet...")
        if not reader.connect():
            print("Error: Failed to connect to Google Sheet")
            print("Please check your Google Sheets URL and authentication")
            sys.exit(1)
        
        # Retrieve work items
        print("Retrieving work items...")
        work_items = reader.retrieve_work_items()
        
        if not work_items:
            print("Error: No work items found for the specified month")
            print("Please check:")
            print(f"1. Are there work items in the '{sheet_name}' sheet?")
            print(f"2. Do the dates in column A match the target month: {target_month.strftime('%B %Y')}?")
            print("3. Are the dates in the correct format (YYYY-MM-DD, MM/DD/YYYY, etc.)?")
            print("Invoice generation cannot continue without work items")
            sys.exit(1)
        
        print(f"Found {len(work_items)} work items")
        
        # Calculate number of rows to insert (X-1 where X is total items)
        num_rows_to_insert = len(work_items) - 1
        if num_rows_to_insert > 0:
            print(f"Adding {num_rows_to_insert} rows at the bottom...")
            if not editor.add_rows_at_bottom(num_rows_to_insert):
                print("Error: Failed to add rows to the Word document")
                print("Cannot continue with invoice generation")
                sys.exit(1)
        
        # Add each working item to the table
        print("Adding working items to the table...")
        for i, item in enumerate(work_items):
            success = editor.add_working_item_to_first_free_row(
                date=item['date'].strftime('%Y-%m-%d'),
                topic=item['topic'],
                efforts=item['working_item'],
                hours=item['hours']
            )
            if not success:
                print(f"Error: Failed to add item {i+1}: {item['topic']}")
                print("Cannot continue with invoice generation")
                sys.exit(1)
        
        # Calculate total hours from all work items
        total_hours = reader.compute_total_hours()
        print(f"Calculated total hours: {total_hours:.2f}")
        
        # Set last row totals
        print("Setting last row totals...")
        if not editor.set_last_row_totals(total_hours):
            print("Error: Failed to set last row totals")
            print("Cannot continue with invoice generation")
            sys.exit(1)
        
        # Format the table with colors and font size
        print("Formatting table...")
        if not editor.format_table():
            print("Error: Failed to format table")
            print("Cannot continue with invoice generation")
            sys.exit(1)
        
        # Display summary
        print(f"\nGoogle Sheets integration completed:")
        print(f"- Added {len(work_items)} working items")
        print(f"- Total hours: {total_hours:.2f}")
        
        # Read currency and hourly rate from Google Sheet
        print("Reading currency and hourly rate from Google Sheet...")
        try:
            currency, hourly_rate = reader.read_currency_and_hourly_rate()
            print(f"Currency from Google Sheet: {currency}")
            print(f"Hourly rate from Google Sheet: {hourly_rate}")
            
            # Check if hourly rate is 0 - this is a critical error
            if hourly_rate == 0.0:
                print("ERROR: Hourly rate is 0.0 - this is a critical error!")
                print("Please check cell E2 in your Google Sheet and ensure it contains a valid hourly rate.")
                sys.exit(1)
            
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        return (total_hours, currency, hourly_rate)
        
    except Exception as e:
        print(f"Error processing Google Sheets data: {e}")
        print("Cannot continue with invoice generation")
        sys.exit(1)

def process_hourly_rate_and_vat(editor, config, total_hours, currency, hourly_rate):
    """
    Process hourly rate and VAT calculations, then replace placeholders.
    
    Args:
        editor (WordDocumentEditor): The Word document editor instance
        config (dict): Configuration dictionary
        total_hours (float): Total hours from Google Sheets
        currency (str): Currency from Google Sheets
        hourly_rate (float): Hourly rate from Google Sheets
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
    print(f"\nProcessing hourly rate and VAT calculations...")
    
    try:
        
        print(f"Currency: {currency}")
        print(f"Hourly rate: {hourly_rate}")
        print(f"Total hours: {total_hours}")
        
        # Check VAT configuration
        vat_enabled = config.get('VAT')
        if vat_enabled is None:
            print("Error: 'VAT' configuration item is missing from config file!")
            sys.exit(1)
        
        # Calculate base amount
        base_amount = total_hours * hourly_rate
        
        # Replace [TOTAL_HOURS] placeholder
        total_hours_replacements = editor.find_and_replace_text("[TOTAL_HOURS]", str(total_hours))
        print(f"Replaced [TOTAL_HOURS] with: {total_hours} ({total_hours_replacements} replacements)")
        
        if vat_enabled:
            print("VAT is enabled - calculating with 8.1% VAT")
            
            # Calculate VAT amount (8.1%)
            vat_amount = base_amount * 0.081
            
            # Calculate total with VAT
            total_with_vat = base_amount + vat_amount
            
            # Format amounts with currency (using proper rounding that rounds 0.5 up)
            from decimal import Decimal, ROUND_HALF_UP
            
            def round_up_half(value, decimals=2):
                """Round value to specified decimal places, rounding 0.5 up"""
                decimal_value = Decimal(str(value))
                return float(decimal_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
            
            vat_formatted = f"{currency} {round_up_half(vat_amount, 2):,.2f}"
            money_no_vat_formatted = f"{currency} {round_up_half(base_amount, 2):,.2f}"
            money_total_formatted = f"{currency} {round_up_half(total_with_vat, 2):,.2f}"
            
            # Replace placeholders
            vat_replacements = editor.find_and_replace_text("[VAT]", vat_formatted)
            money_no_vat_replacements = editor.find_and_replace_text("[MONEY_NO_VAT]", money_no_vat_formatted)
            money_total_replacements = editor.find_and_replace_text("[MONEY_TOTAL]", money_total_formatted)
            
            print(f"Replaced [VAT] with: {vat_formatted} ({vat_replacements} replacements)")
            print(f"Replaced [MONEY_NO_VAT] with: {money_no_vat_formatted} ({money_no_vat_replacements} replacements)")
            print(f"Replaced [MONEY_TOTAL] with: {money_total_formatted} ({money_total_replacements} replacements)")
            
        else:
            print("VAT is disabled - calculating without VAT")
            
            # Format amount with currency
            money_total_formatted = f"{currency} {base_amount:,.2f}"
            
            # Replace placeholder
            money_total_replacements = editor.find_and_replace_text("[MONEY_TOTAL]", money_total_formatted)
            
            print(f"Replaced [MONEY_TOTAL] with: {money_total_formatted} ({money_total_replacements} replacements)")
        
        return True
        
    except Exception as e:
        print(f"Error processing hourly rate and VAT: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate invoice from template')
    parser.add_argument('--config', help='Path to configuration JSON file')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Get template path from config
    template_path = config.get('template')
    if not template_path:
        print("Error: 'template' not found in config file!")
        sys.exit(1)
    
    # Get invoice folder from config
    invoice_folder_base = config.get('invoice_folder')
    if not invoice_folder_base:
        print("Error: 'invoice_folder' not found in config file!")
        sys.exit(1)
    
    try:
        # Initialize Word Document Editor
        print("Initializing Word Document Editor...")
        editor = WordDocumentEditor(template_path)
        
        # Load the document
        print("Loading template document...")
        if not editor.load_document():
            print("Failed to load document!")
            sys.exit(1)
        
        # Get document info
        doc_info = editor.get_document_info()
        print(f"Document loaded: {doc_info['paragraphs_count']} paragraphs, {doc_info['tables_count']} tables")
        
        # Check for custom period configuration for placeholder replacement
        period_from_str = config.get('period_from')
        period_to_str = config.get('period_to')
        custom_period_from = None
        custom_period_to = None
        
        if period_from_str and period_to_str:
            try:
                custom_period_from = WordDocumentEditor.validate_date_format(period_from_str)
                custom_period_to = WordDocumentEditor.validate_date_format(period_to_str)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
        
        # Replace date placeholders
        print("Replacing date placeholders...")
        replacements = editor.replace_date_placeholders(custom_period_from, custom_period_to)
        
        print(f"Replaced [TODAY] with: {WordDocumentEditor.get_today_formatted()} ({replacements['TODAY']} replacements)")
        if custom_period_from and custom_period_to:
            period_display = WordDocumentEditor.format_period_display(custom_period_from, custom_period_to)
            print(f"Replaced [LAST_MONTH] with: {period_display} ({replacements['LAST_MONTH']} replacements)")
        else:
            print(f"Replaced [LAST_MONTH] with: {WordDocumentEditor.get_last_month_formatted()} ({replacements['LAST_MONTH']} replacements)")
        print(f"Replaced [PAY_BY_DATE] with: {WordDocumentEditor.get_pay_by_date_formatted()} ({replacements['PAY_BY_DATE']} replacements)")
        
        if replacements['total'] == 0:
            print("WARNING: No placeholders were found and replaced in the document!")
            print("Please check that the template contains [TODAY], [LAST_MONTH], and/or [PAY_BY_DATE] placeholders.")
        
        # Process Google Sheets data and add working items to the table
        print("\n" + "="*50)
        total_hours, currency, hourly_rate = process_google_sheets_data(editor, config)
        
        # Replace [RATE] placeholder with hourly rate and currency
        print("Replacing [RATE] placeholder...")
        rate_replacements = editor.replace_rate_placeholder(currency, hourly_rate)
        print(f"Replaced [RATE] with: {currency} {hourly_rate:.0f} ({rate_replacements} replacements)")
        
        # Process hourly rate and VAT calculations
        print("\n" + "="*50)
        if not process_hourly_rate_and_vat(editor, config, total_hours, currency, hourly_rate):
            print("Error: Failed to process hourly rate and VAT calculations!")
            sys.exit(1)
        
        # Format payment instruction to bold (after placeholder replacement)
        print("Formatting payment instruction...")
        if not editor.format_payment_instruction():
            print("Warning: Failed to format payment instruction")
            print("Continuing with invoice generation...")
        
        # Create invoice folder
        if custom_period_from and custom_period_to:
            # Use custom period for folder naming
            folder_name = WordDocumentEditor.format_period_folder_name(custom_period_from, custom_period_to)
            invoice_folder = os.path.join(invoice_folder_base, folder_name)
            if not os.path.exists(invoice_folder):
                os.makedirs(invoice_folder)
                print(f"Created invoice folder: {invoice_folder}")
            else:
                print(f"Using existing invoice folder: {invoice_folder}")
            
            # Generate output filename with custom period
            period_display = WordDocumentEditor.format_period_display(custom_period_from, custom_period_to)
            output_filename = editor.generate_output_filename(period_display)
        else:
            # Use default last month for folder naming
            # For default behavior, use current date for folder naming (not last day of previous month)
            today = datetime.now()
            last_month_date = WordDocumentEditor.get_last_month_date()
            
            # Create folder name with current date and last month name
            folder_name = f"{today.strftime('%Y-%m-%d')} {last_month_date.strftime('%B %Y')}"
            invoice_folder = os.path.join(invoice_folder_base, folder_name)
            if not os.path.exists(invoice_folder):
                os.makedirs(invoice_folder)
                print(f"Created invoice folder: {invoice_folder}")
            else:
                print(f"Using existing invoice folder: {invoice_folder}")
            
            # Generate output filename with default last month
            last_month_formatted = WordDocumentEditor.get_last_month_formatted()
            output_filename = editor.generate_output_filename(last_month_formatted)
        output_path = os.path.join(invoice_folder, output_filename)
        
        # Save the document
        print(f"Saving document as '{output_path}'...")
        if editor.save_document(output_path):
            print("Invoice generated successfully!")
            
            # Convert Word document to PDF
            print("\n" + "="*50)
            print("Converting to PDF...")
            if editor.convert_to_pdf(output_path):
                print("PDF conversion completed successfully!")
                
                # Copy PDF to specified folder
                copy_to_folder = config.get('copy_invoice_PDF_to_folder')
                if copy_to_folder:
                    print("\n" + "="*50)
                    print("Copying PDF to specified folder...")
                    
                    # Get the output folder name (last part of the path)
                    output_folder_name = os.path.basename(invoice_folder.rstrip('/'))
                    pdf_path = output_path.replace('.docx', '.pdf')
                    
                    if editor.copy_pdf_to_folder(pdf_path, copy_to_folder, output_folder_name):
                        print("PDF copy completed successfully!")
                    else:
                        print("Warning: PDF copy failed, but PDF was created successfully")
                else:
                    print("No copy folder specified in config, skipping PDF copy")
            else:
                print("Warning: PDF conversion failed, but Word document was saved successfully")
        else:
            print("Failed to save document!")
            sys.exit(1)
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
