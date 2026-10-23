const ITEMS = [
  ["NLP", "Natural Language Processing lets computers work with human text. Here we lowercase the text and remove URLs, HTML tags and punctuation so the model sees clean words."],
  ["TF-IDF", "Term Frequency-Inverse Document Frequency gives each word a score: high if it is frequent in one article but rare across all articles. Each article becomes a vector of these scores."],
  ["Logistic Regression", "A linear model that combines the TF-IDF scores into a probability for each class (FAKE or REAL) using the sigmoid function."],
  ["Passive Aggressive Classifier", "An online linear model: it stays passive when it classifies correctly and updates aggressively when it is wrong. It is fast on large text data. Its scores are calibrated to give probabilities."],
];

export default function About() {
  return (
    <section>
      <h2 className="mb-4 font-serif text-2xl font-bold">About the project</h2>
      <p className="mb-4 text-ink/80">
        Both models are trained on a labeled public dataset and the one with the better validation F1 is used. The result
        reflects writing patterns in that dataset. It cannot check facts, and it can be wrong on new topics, satire or
        misleading context.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        {ITEMS.map(([t, d]) => (
          <div key={t} className="rounded border border-rule bg-white p-4">
            <h3 className="font-semibold">{t}</h3>
            <p className="mt-1 text-sm text-ink/80">{d}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
