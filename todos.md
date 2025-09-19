Copy transport items from GSheet and include them into the calculation of the price

Create a class to read and validate config:

* Company name is in .json name => check for company name as substring in the folder names and template name

Add a validation that all placeholders are in the Word file

* VAT placeholder and MONEY_NO_VAT only if VAT = true in the config

Use constants MONEY_NO_VAT = "[MONEY_NO_VAT]" instead of strings
