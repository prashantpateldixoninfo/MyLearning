import React, { Component } from 'react'

import { movies } from '../movieData';

export class Banner extends Component {
  render() {

    let movieArr=movies.results[Math.floor((Math.random()*10)+1)]

    // let backDrop="/620hnMVLu6RSZW6a5rwO8gqpt0t.jpg";
    let backDrop=movieArr.backdrop_path
    return (      
       <div className="card banner-card" >
       <img src={`https://image.tmdb.org/t/p/original${backDrop}`}
 className="card-img-top banner-img" alt="..."/>
      
         <h5 className="card-title banner-title">Oblivion</h5>
         <p className="card-text  banner-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      
     </div>
    )
  }
}

export default Banner
