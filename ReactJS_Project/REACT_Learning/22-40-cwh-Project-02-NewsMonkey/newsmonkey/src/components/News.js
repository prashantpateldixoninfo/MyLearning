import React, { useState, useEffect } from "react";
import NewsItem from "./NewsItem";
import Spinner from "./Spinner";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";

const News = (props) => {
  document.title = `${props.category.charAt(0).toUpperCase() + props.category.slice(1)} - NewsMonkey`;            

  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);

  const updateNews = async () => {
    props.setProgress(10);
    const url = `https://newsapi.org/v2/top-headlines?country=${props.country}&category=${props.category}&apiKey=${props.apiKey}&page=${page}&pagesize=${props.pageSize}`;

    setLoading(true);
    let data = await fetch(url);
    props.setProgress(30);
    let parsedData = await data.json();
    props.setProgress(70);
    setArticles(parsedData.articles);
    setTotalResults(parsedData.totalResults);
    setLoading(false);
    props.setProgress(100);
  };

  useEffect(() => {
    updateNews();
    // eslint-disable-next-line
  }, []);

  // const handlePrevClick = async () => {
  //   updateNews(page - 1);
  // };

  // const handleNextClick = async () => {
  //   const nextPageNo = page + 1;
  //   if (Math.ceil(totalResults / props.pageSize) > nextPageNo) {
  //     updateNews(nextPageNo);
  //   }
  // };

  const fetchMoreData = async () => {
    const url = `https://newsapi.org/v2/top-headlines?country=${props.country}&category=${props.category}&apiKey=${props.apiKey}&page=${page + 1}&pagesize=${props.pageSize}`;
    setPage(page + 1);
    let data = await fetch(url);
    let parsedData = await data.json();
    setArticles(articles.concat(parsedData.articles));
    setTotalResults(parsedData.totalResults);
  };

  const handleBadgeColor = () => {
    if (props.category === "business") return "primary p-2";
    else if (props.category === "entertainment") return "warning p-2";
    else if (props.category === "general") return "info p-2";
    else if (props.category === "health") return "success p-2";
    else if (props.category === "science") return "danger p-2";
    else if (props.category === "sports") return "dark p-2";
    else if (props.category === "technology") return "danger p-2";
    else return "light p-2";
  };

  return (
    <>
      <h1 className="text-center" style={{ margin: "30px 0px", marginTop: "90px" }}>
        NewsMonkey - Top {props.category.charAt(0).toUpperCase() + props.category.slice(1)} Headlines
      </h1>
      {loading && <Spinner />}
      <InfiniteScroll dataLength={articles.length} next={fetchMoreData} hasMore={articles.length !== totalResults} loader={loading && <Spinner />}>
        <div className="container">
          <div className="row">
            {articles.map((element) => {
              return (
                <div className="col-md-4" key={element.url}>
                  <NewsItem
                    title={element.title ? element.title : ""}
                    description={element.description ? element.description : ""}
                    imgUrl={element.urlToImage}
                    newsUrl={element.url}
                    auther={element.author ? element.author : "Unknown"}
                    date={element.publishedAt ? new Date(element.publishedAt).toGMTString() : "No Date"}
                    source={element.source.name ? element.source.name : "Unknown"}
                    badgeColor={handleBadgeColor()}
                  />
                </div>
              );
            })}
          </div>
        </div>
      </InfiniteScroll>
      {/* <div className="container d-flex justify-content-between">
          <button
            disabled={page <= 1}
            type="button"
            className="btn btn-primary"
            onClick={handlePrevClick}
          >
            &larr; Previous
          </button>
          <button
            disabled={
              Math.ceil(totalResults / props.pageSize) <=
              page + 1
            }
            type="button"
            className="btn btn-primary"
            onClick={handleNextClick}
          >
            Next &rarr;
          </button>
        </div> */}
    </>
  );
};

News.defaultProps = {
  country: "us",
  pageSize: 10,
  category: "general",
};

News.propTypes = {
  country: PropTypes.string,
  pageSize: PropTypes.number,
  category: PropTypes.string,
};
export default News;
