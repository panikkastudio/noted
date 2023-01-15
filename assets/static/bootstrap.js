function init() {
  Alpine.data("noted_actions", (task_id) => ({
    // verdict - one-of [ accept | decline | ignore ]
    async advance(verdict) {
      await fetch("/task/advance", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          verdict,
          id: task_id,
        }),
      });

      window.location.reload();
    },
  }));

  // NER Component
  Alpine.data("noted_ner", (text, spans) => ({
    wrapped: "",

    init() {
      let offset = 0;
      let _wrapped = text;
      console.log(text, spans);

      spans.forEach((span) => {
        const wrapWith = nerAnnotation(span);
        _wrapped = spanWrap(_wrapped, wrapWith, span.start + offset, span.end + offset);
        offset = offset + wrapWith[0].length + wrapWith[1].length;
      });

      this.wrapped = _wrapped;
    },
  }));

  // Classification
  Alpine.data("noted_classification", (text) => ({
    container: {},
  }));

  // NER Manual Component
  Alpine.data("noted_ner_manual", (text, spans, labels) => ({
    labels,

    active_label: labels[0],

    wrapped: "",

    init() {
      let offset = 0;
      let _wrapped = text;
      console.log(text, spans);

      spans.forEach((span) => {
        const wrapWith = nerAnnotation(span);
        _wrapped = spanWrap(_wrapped, wrapWith, span.start + offset, span.end + offset);
        offset = offset + wrapWith[0].length + wrapWith[1].length;
      });

      this.wrapped = _wrapped;
    },

    set_active_label(label) {
      this.active_label = label;
    },
  }));

  // NER Annotation
  Alpine.data("ner_annotation", (span) => ({
    container: {
      // ["style"]: `background-color: ${stringToColor(span.label)}`,
      ["class"]: "task_ner__annotation",
      ["@click"]() {
        console.log(span);
      },
    },
  }));
}

/**
 * Generate nerAnnotation wrapper
 */
function nerAnnotation(span) {
  return [`<mark x-data='ner_annotation(${JSON.stringify(span)})' x-bind="container">`, `<span class="task_ner__label">${span.label}</span></mark>`];
}

/**
 *  Given a string, wrap it at character locations
 *  at start and end.
 */
function spanWrap(str, wrap, start, end) {
  return str.slice(0, start) + wrap[0] + str.substring(start, end) + wrap[1] + str.slice(-1 * (str.length - end));
}

/**
 * Given a string return a hashed color corresponding.
 */
function stringToColor(stringInput) {
  let stringUniqueHash = [...stringInput].reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc);
  }, 0);

  return `hsl(${stringUniqueHash % 360}, 30%, 75%)`;
}
