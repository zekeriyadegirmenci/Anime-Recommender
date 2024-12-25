from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(
    open(
        "/Users/zekeriyadegirmenci/Desktop/other/DemoProject_DSa/data/processed/popular.pkl",
        "rb",
    )
)
pivot_table = pickle.load(
    open(
        "/Users/zekeriyadegirmenci/Desktop/other/DemoProject_DSa/data/processed/pivot_table.pkl",
        "rb",
    )
)
animes = pickle.load(
    open(
        "/Users/zekeriyadegirmenci/Desktop/other/DemoProject_DSa/data/processed/animes.pkl",
        "rb",
    )
)
similarity_scores = pickle.load(
    open(
        "/Users/zekeriyadegirmenci/Desktop/other/DemoProject_DSa/data/processed/similarity_scores.pkl",
        "rb",
    )
)

app = Flask(__name__)

print(popular_df.columns)


@app.route("/")
def index():
    return render_template(
        "index.html",
        book_name=list(popular_df["English name"].values),
        origin_name=list(popular_df["Name"].values),
        image=list(popular_df["Image URL"].values),
        rating=list(popular_df["Score"].values),
    )


@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")


@app.route("/recommend_animes", methods=["post"])
def recommend():
    user_input = request.form.get("user_input")
    index = np.where(pivot_table.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True
    )[1:9]

    data = []
    for i in similar_items:
        item = []
        temp_df = animes[animes["English name"] == pivot_table.index[i[0]]]
        item.extend(
            list(temp_df.drop_duplicates("English name")["English name"].values)
        )
        item.extend(list(temp_df.drop_duplicates("English name")["Other name"].values))
        item.extend(list(temp_df.drop_duplicates("English name")["Image URL"].values))

        data.append(item)

    print(data)

    return render_template("recommend.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
