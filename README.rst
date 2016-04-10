agenda
======

A programmable calendar. One off events can be read from text files in a format
like:

.. code::

  2016-04-10 Write README @todo


Recurrent events can be written in Python, as generators, for example:

.. code:: python

  @register_event
  def readme_anniversary(day):
      readme = date(2016, 4, 10)
      if day.month == readme.month and day.day = readme.day:
          years = readme.year - day.year
          yield "README was written {} years ago today.".format(years)
