# Personal Assistant CLI

## Introduction

Personal Assistant CLI is a command-line interface (CLI) application designed to help you manage your contacts and notes. It allows you to store, search, edit, and delete contacts and notes, ensuring that you have all your important information at your fingertips. The application also includes features for validating phone numbers and email addresses, as well as displaying upcoming birthdays.

## Features

- **Contact Management:**
  - Add new contacts with name, address, phone number(s), email, and birthday.
  - Search contacts by name.
  - Edit contact details.
  - Delete contacts.
  - List all contacts.
  - Display contacts with upcoming birthdays within a specified number of days.
  - Validate phone numbers and email addresses during creation and editing.

- **Note Management:**
  - Add text notes.
  - Search notes by text.
  - Edit notes.
  - Delete notes.

- **Data Persistence:**
  - Automatically save all data to disk.
  - Load data from disk on startup.
  - Autosave after every 5 commands to prevent data loss.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/personal-assistant-cli.git
   cd personal-assistant-cli
