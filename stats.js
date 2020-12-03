!(function ($) {
  "use strict";

  var FILE, LEGEND, ORDER, BALANCE_COLUMNS, HASHRATE_COLUMNS, options, rows;

  FILE = "week.json";

  LEGEND = {
    immature: "Immature Balance",
    unexchanged: "Unexchanged Balance",
    balance: "Balance",
    paid: "Paid Out",
    accepted_rate: "Accepted MH/s",
    rejected_rate: "Rejected MH/s",
  };

  ORDER = [
    "time",
    "immature",
    "unexchanged",
    "balance",
    "paid",
    "accepted",
    "rejected",
  ];

  BALANCE_COLUMNS = ["paid", "balance", "unexchanged", "immature"];

  HASHRATE_COLUMNS = ["rejected", "accepted"];

  options = {
    series: { stack: true, lines: { steps: true, fill: true } },
    xaxis: { mode: "time", timeformat: "%b %e", minTickSize: [1, "day"] },
    legend: { position: "nw" },
  };

  $.getJSON(FILE, function (data) {
    var row, i, len;

    for (i = 0, len = data.length; i < len; ++i) {
      row = data[i];
      row[0] = row[0] * 1000;
    }

    rows = data;

    draw();
  });

  function draw() {
    var column, i, series, len;

    series = [];

    for (i = 0, len = BALANCE_COLUMNS.length; i < len; ++i) {
      column = BALANCE_COLUMNS[i];
      if ($(':checkbox[name="' + column + '"]').is(":checked")) {
        series.push({
          label: LEGEND[column],
          data: rows.map(function (row) {
            return [row[0], row[ORDER.indexOf(column)]];
          }),
          color: i,
          lines: { fill: column !== "paid" },
        });
      }
    }

    $.plot("#balance", series, options);

    series = [];

    for (i = 0, len = HASHRATE_COLUMNS.length; i < len; ++i) {
      column = HASHRATE_COLUMNS[i];

      series.push({
        label: LEGEND[column],
        data: rows
          .filter(function (row) {
            return typeof row[ORDER.indexOf(column)] === "number";
          })
          .map(function (row) {
            return [row[0], row[ORDER.indexOf(column)]];
          }),
      });
    }

    $.plot("#hashrate", series, options);
  }

  $(":checkbox").click(draw);
})(window.jQuery);
