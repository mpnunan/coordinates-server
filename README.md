# Coordinates
Back-end Capstone

## Description

Coordinates is an application intended to simplify wedding seating charts. The intended user is a wedding planner. The user has the ability to manage mulitple events. The user has the ability to share events with multiple other planners, including the ability to share events as read-only or with full editing privilieges.

## Technical Details

The Coordinates API is built with Django and by default utilizes a SQLite database for persistant storage.  In ./coordinates/settings.py, editing the DATABASES list allows easily changing storage to another database, including remote databases hosted elsewhere.

To facilitate access control, Coordinates generates random UUID strings on each entity created. These strings are only passed to users who have been granted full editing privileges, and all update and delete functionality goes through the UUID string. Users with read-only privileges are passed all data except for the UUID string and are therefore unable to send successful POST or PUT requests.

Users are unable to access any data for events which they do not have read or edit privileges.

Permissions are set on the wedding_planner table. The vast majority of functionality passes through this table in some way.

## Installation

Coordinates dependencies are python 3.9, django 4.1.3, djangorestframework 3.14.0, and django-cors-headers 3.13.0
