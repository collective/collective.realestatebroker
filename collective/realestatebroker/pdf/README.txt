PDF export customization
========================

PDF export first appeared in the 2.0 version, so there will be rough
edges. Things that Zest software needed to customize for their initial
customer (which should not end up in the generic product) have been made
customizable. This means that the most common customizations ought to be
possible; there will be room for improvement.

The initial version of the code was copied from Philipp von Weitershausen's
"web component development with zope 3" book.

Customization is done entirely through zope3 utilities. The realestatebroker
code queries for utilities implementing a certain interface and call the
utility if found. Otherwise the defaults apply.

In your own product, add a snippet like this to your configure.zcml::

  <utility component=".layout.modify_stylesheet"
           provides="collective.realestatebroker.pdf.interfaces.IStyleModifier"/>

and, for this example snippet, provide a layout.py with a
`modify_stylesheet()` method.

Style modification
------------------

Use an **IStyleModifier** utility to provide a method that accepts the
existing stylesheet as a parameter and that returns it (modified or
not). Within that method you can change or add to the provided styles.

Page layout
-----------

If an **IHeaderAndFooter** utility is provided it is called with the reportlab
canvas and document as parameters. This way you can add headers and footers
and other generic page components.

Front page
----------

To replace the default front page, provide a **IFrontPage** utility. It gets
passed the current context, request and style. Whatever the utility returns is
added to the output instead of the default front page.

Back matter
-----------

The back matter is handled like the front page, but with a **IBackMatter**
utility. The difference is that there's no default back matter, so everything
is just appended to the end of the PDF. Good for inserting address
information, listing disclaimers, etc.

Fonts
-----

As an example, luxi sans fonts have been included. Use an **IStyleModifier**
utility to add mappings and to change the styles to use those fonts. With
fonts you ought to be real careful of copyrights and licenses, btw.

The Luxi TrueType fonts (luxis*.ttf) provided in this package are
Copyright (c) 2001 by Bigelow & Holmes Inc.  See COPYRIGHT.BH for
further information.

Editor note
-----------

Note: this is the `pdf/README.txt` inside the realestatebroker product. So
don't edit it directly on plone.org, but in svn.