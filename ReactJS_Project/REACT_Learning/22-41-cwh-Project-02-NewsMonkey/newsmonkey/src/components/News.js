import React, { Component } from "react";
import NewsItem from "./NewsItem";
import Spinner from "./Spinner";
import PropTypes from "prop-types";

export class News extends Component {
  articles = [
    {
      source: {
        id: "cbs-news",
        name: "CBS News",
      },
      author: "S. Dev",
      title:
        "Several U.S. service members injured in missile attack at Al-Asad Airbase in Iraq, Pentagon says - CBS News",
      description:
        "Monday's strike was the 66th attack against American-affiliated bases in Iraq and Syria since Oct. 17, Pentagon officials said.",
      url: "https://www.cbsnews.com/news/us-service-members-injured-missile-attack-al-asad-airbase-iraq/",
      urlToImage:
        "https://assets3.cbsnewsstatic.com/hub/i/r/2023/11/21/dc9d7318-8630-41b5-9f94-99edf83b06fb/thumbnail/1200x630/15bd9987ca1d88708be5599d03343b08/gettyimages-458175702.jpg?v=5659e73acd91751548aa89950cf015b0",
      publishedAt: "2023-11-22T03:55:00Z",
      content:
        "Several U.S. service members were injured in a ballistic missile attack by Iranian-backed militias on Al-Asad Airbase in Iraq, Pentagon officials said Tuesday.  \r\nThe attack Monday night on U.S. and … [+3282 chars]",
    },
    {
      source: {
        id: "associated-press",
        name: "Associated Press",
      },
      author: "JOSEF FEDERMAN, JACK JEFFERY",
      title:
        "Israel approves cease-fire with Hamas: 50 hostages released - The Associated Press",
      description:
        "Qatar has announced a truce-for-hostages deal between Israel and Hamas that would bring a four-day halt in fighting in a devastating six-week war. The deal would win freedom for 50 hostages held in the Gaza Strip and also lead to the release of Palestinian pr…",
      url: "https://apnews.com/article/israel-hamas-war-news-11-21-2023-39f5ae0bdb4e32f0e69115aa43446132",
      urlToImage:
        "https://dims.apnews.com/dims4/default/5c2233b/2147483647/strip/true/crop/8313x4676+0+433/resize/1440x810!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F2a%2Fea%2Fe567b0cc25ec9d4210531e80a454%2F1f52228c8fcc476c87e64131a10c949a",
      publishedAt: "2023-11-22T03:52:00Z",
      content:
        "JERUSALEM (AP) Qatar on Wednesday announced a truce-for-hostages deal between Israel and Hamas that would bring the first temporary halt in fighting in a devastating six-week war, win freedom for doz… [+9825 chars]",
    },
    {
      source: {
        id: "cnn",
        name: "CNN",
      },
      author: "Lauren del Valle, Kara Scannell",
      title:
        "Former Trump Org. controller breaks down in tears on witness stand in fraud trial - CNN",
      description:
        "After four days of testimony and two trips to the witness stand, former Trump Organization controller Jeff McConney broke down in tears on Tuesday, telling the court the toll of the numerous investigations and accusations of misconduct drove him to leave the …",
      url: "https://www.cnn.com/2023/11/21/politics/mcconney-trump-org-testimony-fraud-trial/index.html",
      urlToImage:
        "https://media.cnn.com/api/v1/images/stellar/prod/ap23325676357690.jpg?c=16x9&q=w_800,c_fill",
      publishedAt: "2023-11-22T03:24:00Z",
      content:
        "After four days of testimony and two trips to the witness stand, former Trump Organization controller Jeff McConney broke down in tears on Tuesday, telling the court the toll of the numerous investig… [+3733 chars]",
    },
    {
      source: {
        id: null,
        name: "Variety",
      },
      author: "Emily Longeretta",
      title:
        "'Dancing With the Stars' Taylor Swift Night: Harry Jowsey Eliminated - Variety",
      description:
        "The 'Dancing With the Stars' semi-finalists were revealed after Taylor Swift night.",
      url: "https://variety.com/lists/dancing-with-the-stars-taylor-swift-night-harry-jowsey-eliminated/",
      urlToImage:
        "https://variety.com/wp-content/uploads/2023/11/404308052_7201731949845964_1313361528302771450_n.jpg?w=823&h=563&crop=1",
      publishedAt: "2023-11-22T03:02:00Z",
      content:
        "It feels like the perfect night… to send another couple home. On Tuesday night’s “Dancing With the Stars,” each pair took on a Taylor Swift song. Mandy Moore, the lead choreographer on the “Eras Tour… [+927 chars]",
    },
  ];

  static defaultProps = {
    country: "us",
    pageSize: 10,
    category: "general",
  };

  static propTypes = {
    country: PropTypes.string,
    pageSize: PropTypes.number,
    category: PropTypes.string,
  };

  constructor() {
    super();
    this.state = {
      page: 1,
      articles: [], //this.articles,
      totalArticles: 0,
      loading: false,
    };
  }

  async updateNews(pageNo) {
    const url = `https://newsapi.org/v2/top-headlines?country=${this.props.country}&category=${this.props.category}&apiKey=9f8c2bef75eb45fa9d6c27cfe78a077e&page=${pageNo}&pagesize=${this.props.pageSize}`;

    this.setState({ loading: true });
    let data = await fetch(url);
    let parsedData = await data.json();
    this.setState({
      page: pageNo,
      articles: parsedData.articles,
      totalArticles: parsedData.totalResults,
      loading: false,
    });
  }

  async componentDidMount() {
    this.updateNews(1);
  }

  handlePrevClick = async () => {
    this.updateNews(this.state.page - 1);
  };

  handleNextClick = async () => {
    const nextPageNo = this.state.page + 1;
    if (
      Math.ceil(this.state.totalArticles / this.props.pageSize) > nextPageNo
    ) {
      this.updateNews(nextPageNo);
    }
  };

  handleBadgeColor = () => {
    if (this.props.category === "business") return "primary p-2";
    else if (this.props.category === "entertainment") return "warning p-2";
    else if (this.props.category === "general") return "info p-2";
    else if (this.props.category === "health") return "success p-2";
    else if (this.props.category === "science") return "danger p-2";
    else if (this.props.category === "sports") return "dark p-2";
    else if (this.props.category === "technology") return "danger p-2";
    else return "light p-2";
  };

  render() {
    return (
      <div className="container my-3">
        <h1 className="text-center" style={{ margin: "30px 0px" }}>
          NewsMonkey - Top Headlines
        </h1>
        {this.state.loading && <Spinner />}
        <div className="row">
          {!this.state.loading &&
            this.state.articles.map((element) => {
              return (
                <div className="col-md-4" key={element.url}>
                  <NewsItem
                    title={element.title ? element.title : ""}
                    description={element.description ? element.description : ""}
                    imgUrl={element.urlToImage}
                    newsUrl={element.url}
                    auther={element.author ? element.author : "Unknown"}
                    date={
                      element.publishedAt
                        ? new Date(element.publishedAt).toGMTString()
                        : "No Date"
                    }
                    source={
                      element.source.name ? element.source.name : "Unknown"
                    }
                    badgeColor={this.handleBadgeColor()}
                  />
                </div>
              );
            })}
        </div>
        <div className="container d-flex justify-content-between">
          <button
            disabled={this.state.page <= 1}
            type="button"
            className="btn btn-primary"
            onClick={this.handlePrevClick}
          >
            &larr; Previous
          </button>
          <button
            disabled={
              Math.ceil(this.state.totalArticles / this.props.pageSize) <=
              this.state.page + 1
            }
            type="button"
            className="btn btn-primary"
            onClick={this.handleNextClick}
          >
            Next &rarr;
          </button>
        </div>
      </div>
    );
  }
}

export default News;
