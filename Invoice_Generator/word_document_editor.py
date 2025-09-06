#!/usr/bin/env python3
"""
Word Document Editor Class
Handles Word document template processing, placeholder replacement, and document manipulation.
"""

import os
from datetime import datetime, timedelta
from docx import Document
from typing import Dict, List, Optional

class WordDocumentEditor:
    """
    A class to handle Word document template processing and editing.
    
    Attributes:
        template_path (str): Path to the Word document template
        document (Document): The loaded Word document
    """
    
    def __init__(self, template_path: str):
        """
        Initialize the WordDocumentEditor.
        
        Args:
            template_path (str): Path to the Word document template
        """
        self.template_path = template_path
        self.document = None
        self._validate_template()
    
    def _validate_template(self):
        """Validate that the template file exists and is accessible."""
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file '{self.template_path}' not found!")
    
    def load_document(self) -> bool:
        """
        Load the Word document template.
        
        Returns:
            bool: True if document loaded successfully, False otherwise
        """
        try:
            self.document = Document(self.template_path)
            return True
        except Exception as e:
            print(f"Error loading document: {e}")
            return False
    
    @staticmethod
    def get_today_formatted() -> str:
        """Get today's date in MMMM dd, YYYY format"""
        return datetime.now().strftime("%B %d, %Y")
    
    @staticmethod
    def get_last_month_formatted() -> str:
        """Get last month in MMMM YYYY format"""
        today = datetime.now()
        # Get first day of current month, then subtract one day to get last month
        first_day_current = today.replace(day=1)
        last_month = first_day_current - timedelta(days=1)
        return last_month.strftime("%B %Y")
    
    @staticmethod
    def get_pay_by_date_formatted() -> str:
        """Get today + 30 days in MMMM dd, YYYY format"""
        today = datetime.now()
        pay_by_date = today + timedelta(days=30)
        return pay_by_date.strftime("%B %d, %Y")
    
    @staticmethod
    def get_last_month_date() -> datetime:
        """Get last month date object for folder naming"""
        today = datetime.now()
        first_day_current = today.replace(day=1)
        return first_day_current - timedelta(days=1)
    
    def find_and_replace_text(self, old_text: str, new_text: str) -> int:
        """
        Find and replace text in all paragraphs and tables.
        
        Args:
            old_text (str): Text to find and replace
            new_text (str): Text to replace with
            
        Returns:
            int: Number of replacements made
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        replacements_made = 0
        
        # Replace in paragraphs
        for paragraph in self.document.paragraphs:
            if old_text in paragraph.text:
                # Clear the paragraph and rebuild it with the replacement
                full_text = paragraph.text
                if old_text in full_text:
                    paragraph.clear()
                    paragraph.add_run(full_text.replace(old_text, new_text))
                    replacements_made += 1
        
        # Replace in tables
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if old_text in paragraph.text:
                            # Clear the paragraph and rebuild it with the replacement
                            full_text = paragraph.text
                            if old_text in full_text:
                                paragraph.clear()
                                paragraph.add_run(full_text.replace(old_text, new_text))
                                replacements_made += 1
        
        return replacements_made
    
    def replace_date_placeholders(self) -> Dict[str, int]:
        """
        Replace all date placeholders in the document.
        
        Returns:
            Dict[str, int]: Dictionary with placeholder names and replacement counts
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        # Get formatted dates
        today_formatted = self.get_today_formatted()
        last_month_formatted = self.get_last_month_formatted()
        pay_by_date_formatted = self.get_pay_by_date_formatted()
        
        # Replace placeholders
        today_replacements = self.find_and_replace_text("[TODAY]", today_formatted)
        last_month_replacements = self.find_and_replace_text("[LAST_MONTH]", last_month_formatted)
        pay_by_date_replacements = self.find_and_replace_text("[PAY_BY_DATE]", pay_by_date_formatted)
        
        return {
            "TODAY": today_replacements,
            "LAST_MONTH": last_month_replacements,
            "PAY_BY_DATE": pay_by_date_replacements,
            "total": today_replacements + last_month_replacements + pay_by_date_replacements
        }
    
    def add_table_entries(self, table_name: str, entries: List[Dict]) -> bool:
        """
        Add entries to a specific table in the document.
        
        Args:
            table_name (str): Name or identifier of the table to find
            entries (List[Dict]): List of entries to add, each with keys: date, topic, efforts, hours
            
        Returns:
            bool: True if entries were added successfully, False otherwise
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        # Find the table (simplified - assumes first table for now)
        table = None
        for t in self.document.tables:
            table = t
            break
        
        if not table:
            print(f"Warning: Could not find table '{table_name}'")
            return False
        
        try:
            # Add new entries after the header row (first row)
            for entry in entries:
                new_row = table.add_row()
                new_row.cells[0].text = entry.get('date', '')
                new_row.cells[1].text = entry.get('topic', '')
                new_row.cells[2].text = entry.get('efforts', '')
                new_row.cells[3].text = str(entry.get('hours', 0))
            
            print(f"Added {len(entries)} entries to the table")
            return True
            
        except Exception as e:
            print(f"Error adding table entries: {e}")
            return False
    
    def add_rows_before_last_row(self, num_rows: int) -> bool:
        """
        Find the first table and add X rows before the last row.
        
        Args:
            num_rows (int): Number of rows to add before the last row
            
        Returns:
            bool: True if rows were added successfully, False otherwise
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        # Find the first table
        if not self.document.tables:
            print("Warning: No tables found in the document")
            return False
        
        table = self.document.tables[0]
        
        try:
            # Get the number of existing rows
            total_rows = len(table.rows)
            
            if total_rows < 2:
                print("Warning: Table has less than 2 rows, cannot add rows before last row")
                return False
            
            print(f"Table has {total_rows} rows, adding {num_rows} rows before the last row")
            
            # Get the last row to copy its structure
            last_row = table.rows[total_rows - 1]
            num_cols = len(last_row.cells)
            
            # Simple approach: just add rows at the end
            # This is more reliable than trying to insert in specific positions
            for i in range(num_rows):
                new_row = table.add_row()
                # Ensure the new row has the same number of cells as other rows
                while len(new_row.cells) < num_cols:
                    new_row._element.append(new_row._element._new_tc())
            
            print(f"Successfully added {num_rows} rows to the table")
            print(f"Table now has {len(table.rows)} rows")
            return True
            
        except Exception as e:
            print(f"Error adding rows to table: {e}")
            return False
    
    def add_working_item_to_first_free_row(self, date: str, topic: str, efforts: str, hours: float) -> bool:
        """
        Add a working item to the first free row from the top in the first table.
        
        Args:
            date (str): Date of the work item
            topic (str): Topic of the work item
            efforts (str): Description of efforts/work done
            hours (float): Number of hours worked
            
        Returns:
            bool: True if item was added successfully, False otherwise
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        # Find the first table
        if not self.document.tables:
            print("Warning: No tables found in the document")
            return False
        
        table = self.document.tables[0]
        
        try:
            # Find the first free row (starting from row 1, skipping header row 0)
            free_row_index = None
            
            for row_idx in range(1, len(table.rows)):
                # Check if the first cell (date column) is empty
                first_cell_text = table.rows[row_idx].cells[0].text.strip()
                if not first_cell_text:
                    free_row_index = row_idx
                    break
            
            # If no free row found, add a new row at the end
            if free_row_index is None:
                new_row = table.add_row()
                free_row_index = len(table.rows) - 1
            
            # Fill the free row with the working item data
            row = table.rows[free_row_index]
            
            # Ensure the row has enough cells
            while len(row.cells) < 4:
                row._element.append(row._element._new_tc())
            
            # Set the cell values
            row.cells[0].text = str(date)
            row.cells[1].text = str(topic)
            row.cells[2].text = str(efforts)
            row.cells[3].text = str(hours)
            
            print(f"Added working item to row {free_row_index + 1}: {date} - {topic}")
            return True
            
        except Exception as e:
            print(f"Error adding working item to table: {e}")
            return False
    
    def save_document(self, output_path: str) -> bool:
        """
        Save the document to the specified path.
        
        Args:
            output_path (str): Path where to save the document
            
        Returns:
            bool: True if document saved successfully, False otherwise
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Validate document before saving
            if not self._validate_document():
                print("Warning: Document validation failed, but attempting to save anyway...")
            
            # Save the document
            self.document.save(output_path)
            
            # Set proper file permissions (readable and writable by owner)
            import stat
            os.chmod(output_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            
            # Verify the file was created and is readable
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"Document saved successfully: {output_path}")
                print(f"File size: {os.path.getsize(output_path)} bytes")
                return True
            else:
                print(f"Error: Document was not saved properly or file is empty")
                return False
                
        except Exception as e:
            print(f"Error saving document: {e}")
            print(f"Output path: {output_path}")
            print(f"Directory exists: {os.path.exists(os.path.dirname(output_path))}")
            return False
    
    def get_template_filename(self) -> str:
        """
        Get the template filename.
        
        Returns:
            str: The template filename
        """
        return os.path.basename(self.template_path)
    
    def generate_output_filename(self, last_month_formatted: str) -> str:
        """
        Generate output filename by replacing [LAST_MONTH] in template filename.
        
        Args:
            last_month_formatted (str): Formatted last month string
            
        Returns:
            str: Generated output filename
        """
        template_filename = self.get_template_filename()
        return template_filename.replace("[LAST_MONTH]", last_month_formatted)
    
    def get_document_info(self) -> Dict[str, str]:
        """
        Get information about the loaded document.
        
        Returns:
            Dict[str, str]: Document information
        """
        if not self.document:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "template_path": self.template_path,
            "paragraphs_count": len(self.document.paragraphs),
            "tables_count": len(self.document.tables)
        }
    
    def read_table_cell(self, row: int, col: int) -> str:
        """
        Read a specific cell from the first table.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based, where A=0, B=1, C=2, D=3, E=4)
            
        Returns:
            str: Cell content as string
            
        Raises:
            ValueError: If table doesn't exist or cell is out of bounds
        """
        if not self.document:
            raise ValueError("Document not loaded. Call load_document() first.")
        
        if not self.document.tables:
            raise ValueError("No tables found in the document")
        
        table = self.document.tables[0]
        
        if row >= len(table.rows):
            raise ValueError(f"Row {row} is out of bounds. Table has {len(table.rows)} rows.")
        
        row_obj = table.rows[row]
        
        if col >= len(row_obj.cells):
            raise ValueError(f"Column {col} is out of bounds. Row has {len(row_obj.cells)} columns.")
        
        return row_obj.cells[col].text.strip()
    
    def _validate_document(self) -> bool:
        """
        Validate the document structure before saving.
        
        Returns:
            bool: True if document is valid, False otherwise
        """
        if not self.document:
            return False
        
        try:
            # Check if document has content
            if len(self.document.paragraphs) == 0 and len(self.document.tables) == 0:
                print("Warning: Document appears to be empty")
                return False
            
            # Check for any obvious corruption indicators
            for paragraph in self.document.paragraphs:
                if paragraph.text and len(paragraph.text) > 10000:  # Very long paragraphs might indicate corruption
                    print("Warning: Found unusually long paragraph, possible corruption")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Document validation error: {e}")
            return False
