#!/bin/sh
PRODUCTNAME='collective.realestatebroker'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --merge locales/${PRODUCTNAME}-manual.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/nl/LC_MESSAGES/${PRODUCTNAME}.po
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/il/LC_MESSAGES/${PRODUCTNAME}.po
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/fr/LC_MESSAGES/${PRODUCTNAME}.po

# compile mo file
msgfmt -o locales/nl/LC_MESSAGES/${PRODUCTNAME}.mo locales/nl/LC_MESSAGES/${PRODUCTNAME}.po
msgfmt -o locales/il/LC_MESSAGES/${PRODUCTNAME}.mo locales/il/LC_MESSAGES/${PRODUCTNAME}.po
msgfmt -o locales/il/LC_MESSAGES/${PRODUCTNAME}.mo locales/fr/LC_MESSAGES/${PRODUCTNAME}.po
