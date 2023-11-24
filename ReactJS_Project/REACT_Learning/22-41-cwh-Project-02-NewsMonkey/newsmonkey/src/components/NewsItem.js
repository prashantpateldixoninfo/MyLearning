import React, { Component } from "react";

export class NewsItem extends Component {
  render() {
    let { title, description, imgUrl, newsUrl, auther, date, source, badgeColor } =
      this.props;
    return (
      <div className="my-3">
        <div className="card">
          <span
            className={`position-absolute top-0 translate-middle badge rounded-pill bg-${badgeColor}`}
            style={{ zIndex: 1, left: "90%" }}
          >
            {source}
          </span>
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
  }
}

export default NewsItem;
