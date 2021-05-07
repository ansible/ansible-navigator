
The following table describes all available configuration options.
Note that all options here must be specified under the ``ansible-navigator``
outer key and that options with ``.`` in them specify suboptions. Thus,
``log.level`` below could be configured like this:

.. code-block:: yaml

    ansible-navigator:
      log:
        level: debug

..
  start-parameter-table

.. list-table:: Frozen Delights!
  :widths: 15 10 30
  :header-rows: 1

  * - Treat
    - Quantity
    - Description
  * - Albatross
    - 2.99
    - On a stick!
  * - Crunchy Frog
    - 1.49
    - If we took the bones out, it wouldn't be
      crunchy, now would it?
  * - Gannet Ripple
    - 1.99
    - On a stick!