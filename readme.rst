===========
ARISTOXENUS
===========

Musical manipulation tool.

Subtitle
--------

Sub-subtitle
------------

Just learning some RST [#]_

.. [#] This is an autonumbered footnote

Learning a few things [2]_

.. [2] This is a manual footnote

And again... [#]_

.. [#] This is another autonumbered footnote

Emphasis *like this*

**STRONG**

``literal``


This is regular text\ :sub:`this is subscript text`\ this is regular text again

We can make a substitution for |TEXT|

.. |TEXT| replace:: text\ :sub:`subscript`\

+----------+-----------+------------+
| HEADER 1 |           |            |
+==========+===========+============+
| body 1   |      body2|  body 3    |
+----------+-----------+------------+
|                      |     boobs  |
|      boobs           |            |
+----------------------+------------+



Definition Heading
    This is a Definition

:Field Heading:
    This is a block of text for a Field
    We can keep the indentation
        Or even increase it.
    And return back

:Field Heading 2: This one is short!

Maybe I need nest before options for it to work.

-a         Output all.
-b         Output both (this description is
           quite long).
-c arg     Output just arg.
--long     Output all day long.
-gnnd      TEST

-p         This option has two paragraphs in the description.
           This is the first.

           This is the second.  Blank lines may be omitted between
           options (as above) or left in (as here and below).

--very-long-option  A VMS-style option.  Note the adjustment for
                    the required two spaces.

--an-even-longer-option
           The description can also start on the next line.

-2, --two  This option has two variants.

-f FILE, --file=FILE  These two options are synonyms; both have
                      arguments.

/V         A VMS/DOS-style option.

An enumerated list

1. Some items are given explicit numbers
2. We don't have to keep sequence
#. But we can also auto-number items


Bullet list

- item 1
- item 2
+ item 3
* item 4