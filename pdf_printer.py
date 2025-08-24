#!/usr/bin/env python3
"""
PDF Network Printer Module
Prints PDF files to network printers with proper parameters:
- Single-sided printing (no duplex)
- A4 paper size
- Fit-to-page scaling
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


class NetworkPDFPrinter:
    """Handle printing PDFs to network printers with specific parameters."""
    
    def __init__(self):
        self.supported_systems = ['darwin', 'linux', 'win32']
        self.system = sys.platform
        
    def get_available_printers(self):
        """Get list of available network printers."""
        try:
            if self.system == 'darwin':  # macOS
                result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
                if result.returncode == 0:
                    printers = []
                    for line in result.stdout.split('\n'):
                        if line.startswith('printer '):
                            printer_name = line.split()[1]
                            printers.append(printer_name)
                    return printers
            
            elif self.system == 'linux':  # Linux
                result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
                if result.returncode == 0:
                    printers = []
                    for line in result.stdout.split('\n'):
                        if line.startswith('printer '):
                            printer_name = line.split()[1]
                            printers.append(printer_name)
                    return printers
                    
            elif self.system == 'win32':  # Windows
                result = subprocess.run(['wmic', 'printer', 'get', 'name'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    printers = []
                    lines = result.stdout.split('\n')[1:]  # Skip header
                    for line in lines:
                        line = line.strip()
                        if line and line != 'Name':
                            printers.append(line)
                    return printers
                    
        except FileNotFoundError:
            print("Error: Required printing tools not found on this system")
            
        return []
    
    def print_pdf(self, pdf_path, printer_name, copies=1):
        """
        Print PDF to specified network printer with proper parameters.
        
        Args:
            pdf_path: Path to PDF file
            printer_name: Name of the network printer
            copies: Number of copies to print (default: 1)
            
        Returns:
            bool: True if printing was successful, False otherwise
        """
        
        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found: {pdf_path}")
            return False
            
        print(f"Printing PDF: {pdf_path}")
        print(f"Printer: {printer_name}")
        print(f"Copies: {copies}")
        print("Settings: Single-sided, A4, fit-to-page")
        print("-" * 50)
        
        try:
            if self.system == 'darwin':  # macOS
                cmd = [
                    'lpr',
                    '-P', printer_name,
                    '-o', 'media=A4',           # A4 paper size
                    '-o', 'sides=one-sided',    # Single-sided printing
                    '-o', 'fit-to-page',        # Scale to fit page
                    '-o', 'orientation-requested=3',  # Portrait
                    '-#', str(copies),          # Number of copies
                    pdf_path
                ]
                
            elif self.system == 'linux':  # Linux
                cmd = [
                    'lpr',
                    '-P', printer_name,
                    '-o', 'media=A4',           # A4 paper size
                    '-o', 'sides=one-sided',    # Single-sided printing
                    '-o', 'fit-to-page',        # Scale to fit page
                    '-o', 'orientation-requested=3',  # Portrait
                    '-#', str(copies),          # Number of copies
                    pdf_path
                ]
                
            elif self.system == 'win32':  # Windows
                # Windows printing using command line
                cmd = [
                    'powershell.exe', '-Command',
                    f'Start-Process -FilePath "{pdf_path}" -ArgumentList "/p /h" -WindowStyle Hidden'
                ]
                
            # Execute printing command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✔ PDF sent to printer successfully")
                if result.stdout:
                    print(f"Output: {result.stdout}")
                return True
            else:
                print(f"✖ Printing failed with return code: {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
                
        except FileNotFoundError as e:
            print(f"Error: Required printing command not found: {e}")
            return False
        except Exception as e:
            print(f"Error: Printing failed: {e}")
            return False
    
    def print_status(self, printer_name=None):
        """Check printer status and queue."""
        try:
            if printer_name:
                if self.system in ['darwin', 'linux']:
                    cmd = ['lpq', '-P', printer_name]
                else:  # Windows
                    return "Printer status checking not implemented for Windows"
            else:
                if self.system in ['darwin', 'linux']:
                    cmd = ['lpq']
                else:  # Windows
                    return "Printer status checking not implemented for Windows"
                    
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error checking printer status: {result.stderr}"
                
        except FileNotFoundError:
            return "Error: lpq command not found"
        except Exception as e:
            return f"Error: {e}"


def main():
    """Command-line interface for PDF printing."""
    parser = argparse.ArgumentParser(
        description="Print PDF files to network printers with proper A4 single-sided settings"
    )
    parser.add_argument(
        "pdf_path", 
        nargs='?',
        help="Path to PDF file to print"
    )
    parser.add_argument(
        "-p", "--printer", 
        help="Printer name (use --list to see available printers)"
    )
    parser.add_argument(
        "-c", "--copies", 
        type=int, 
        default=1,
        help="Number of copies to print (default: 1)"
    )
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List available printers"
    )
    parser.add_argument(
        "--status", 
        action="store_true",
        help="Check printer queue status"
    )
    
    args = parser.parse_args()
    
    printer = NetworkPDFPrinter()
    
    # List printers
    if args.list:
        print("Available printers:")
        printers = printer.get_available_printers()
        if printers:
            for p in printers:
                print(f"  • {p}")
        else:
            print("  No printers found")
        return
    
    # Check printer status
    if args.status:
        status = printer.print_status(args.printer)
        print("Printer Queue Status:")
        print(status)
        return
    
    # Print PDF
    if not args.pdf_path:
        print("Error: PDF path is required for printing")
        parser.print_help()
        sys.exit(1)
    
    if not args.printer:
        print("Error: Printer name is required")
        print("Use --list to see available printers")
        sys.exit(1)
    
    # Verify printer exists
    available_printers = printer.get_available_printers()
    if args.printer not in available_printers:
        print(f"Error: Printer '{args.printer}' not found")
        print("Available printers:")
        for p in available_printers:
            print(f"  • {p}")
        sys.exit(1)
    
    # Print the PDF
    success = printer.print_pdf(args.pdf_path, args.printer, args.copies)
    
    if success:
        print(f"\n🖨️  Print job sent successfully!")
        print("💡 Settings applied: Single-sided, A4 paper, fit-to-page")
    else:
        print("\n❌ Print job failed")
        sys.exit(1)


if __name__ == "__main__":
    main()