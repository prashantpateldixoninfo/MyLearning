import { useEffect, useState } from "react";
import "./App.css";
import logo from "./logo.svg";
import Skeleton from "./skeleton/Skeleton";

function App() {
    const [loadingState, setLoadingState] = useState(false);

    useEffect(() => {
        setTimeout(() => {
            setLoadingState(true);
        }, 2000);
    });

    const contentBlockData = () => {
        console.log(loadingState);

        if (loadingState) {
            return [...Array(3)].map((item, index) => {
                return (
                    <div key={index}>
                        <h2>What is Lorem Ipsum?</h2>
                        <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry.</p>
                    </div>
                );
            });
        } else {
            return [...Array(3)].map((item, index) => {
                return (
                    <div className="skeletonBlock" key={index}>
                        <Skeleton width="300px" height="40px" />
                        <Skeleton height="20px" variant="paragraph" />
                        <Skeleton height="20px" variant="paragraph" />
                        <Skeleton height="20px" variant="paragraph" />
                        <Skeleton height="20px" width="50%" variant="paragraph" />
                    </div>
                );
            });
        }
    };

    const cardBlockData = () => {
        if (loadingState) {
            return [...Array(4)].map((item, index) => {
                return (
                    <div className="card">
                        <div className="cardImage">
                            <img src={logo} alt="logo" width="80px" height="80px" />
                            <div>The React App</div>
                        </div>
                        <div className="cardSkeletonTitle">
                            <h2>What is Lorem ?</h2>
                        </div>
                        <div className="cardSkeletonBody">
                            <p>
                                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown
                                printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting,
                                remaining essentially unchanged. It was popularised in the 1960s with the release of Letra
                            </p>
                        </div>
                    </div>
                );
            });
        } else {
            return [...Array(4)].map((index, item) => {
                return (
                    <div className="cardSkeleton">
                        <div className="cardSkeletonImage">
                            <Skeleton width="80px" height="80px" variant="circle" />
                            <Skeleton width="100%" height="20px" />
                        </div>
                        <div className="cardSkeletonTitle">
                            <Skeleton width="100%" height="30px" />
                        </div>
                        <div className="cardSkeletonBody">
                            <Skeleton width="250px" height="300px" />
                        </div>
                    </div>
                );
            });
        }
    };

    return (
        <div className="App">
            <h1>React Skeleton Loading Tutorial</h1>
            <div>
                <h2>Heading Skeleton</h2>
                {loadingState ? (
                    <div className="heading">
                        <h1>Heading 1</h1>
                        <h2>Heading 2</h2>
                        <h3>Heading 3</h3>
                    </div>
                ) : (
                    <div className="skeletonBlock">
                        <Skeleton width="200px" height="38px" />
                        <Skeleton width="150px" height="28px" />
                        <Skeleton width="100px" height="25px" />
                    </div>
                )}
            </div>
            <div>
                <h2>Content Skeleton</h2>
                <div className="contentBlock">{contentBlockData()}</div>
            </div>
            <div>
                <h2>Card Skeleton</h2>
                <div className="cardBlock">{cardBlockData()}</div>
            </div>
        </div>
    );
}

export default App;
