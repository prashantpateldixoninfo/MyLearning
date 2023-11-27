import React from "react";

const NewsItem = (props) => {
  let {
    title,
    description,
    imgUrl,
    newsUrl,
    auther,
    date,
    source,
    badgeColor,
  } = props;

  return (
    <div className="my-3">
      <div className="card">
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            position: "absolute",
            right: 0,
          }}
        >
          <span className={`badge rounded-pill bg-${badgeColor}`}>
            {source}
          </span>
        </div>
        <img
          src={imgUrl ? imgUrl : require("./../images/noImg.png")}
          className="card-img-top"
          alt="..."
        />
        <div className="card-body">
          <h5 className="card-title">{title}...</h5>
          <p className="card-text">{description}...</p>
          <p className="card-text">
            <small className={`bg-light text-danger-emphasis`}>
              By {auther} on {date}
            </small>
          </p>
          <a
            href={newsUrl}
            target="_blank"
            rel="noreferrer"
            className="btn btn-sm btn-dark"
          >
            Read More
          </a>
        </div>
      </div>
    </div>
  );
};

export default NewsItem;
