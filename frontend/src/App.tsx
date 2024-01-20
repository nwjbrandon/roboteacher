import React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';
import axios from 'axios';
import ReactAudioPlayer from 'react-audio-player';
import BounceLoader from 'react-spinners/BounceLoader';
import TimeAgo from 'react-timeago';
import moment from 'moment';
import './App.css';

const BACKEND_URL: string | undefined = process.env.REACT_APP_BACKEND_URL;

type OptionType = {
  option: string;
  is_answer: boolean;
};

type ArticleType = {
  url: string;
  title: string;
  content: string;
  translated: string;
  question: string;
  options: OptionType[];
  audioObjectKey: string;
  createdAt: string;
};

type ArticlesType = {
  articles: ArticleType[];
};

type BodyResponse = {
  body: ArticlesType;
};

type DataResponse = {
  data: BodyResponse;
};

const fetchReadingPassages = async () => {
  if (BACKEND_URL === undefined) {
    return;
  }
  try {
    const res: DataResponse = await axios.post<BodyResponse>(BACKEND_URL, {
      task: 'fetch_data'
    });
    const articles: ArticleType[] = res.data.body.articles;
    return articles;
  } catch (error) {
    console.log(error);
    return;
  }
};

interface ArticleProps {
  articleIdx: number;
  article: ArticleType;
}

const Article: React.FC<ArticleProps> = ({ articleIdx, article }) => {
  const [isHidden, setIsHidden] = React.useState<boolean>(true);
  const [userAnswer, setUserAnswer] = React.useState<number>(-1);
  const time = moment.utc(article.createdAt).toDate();

  const handleVisibilityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIsHidden(event.target.checked);
  };

  return (
    <div>
      <div className="article-title">
        <div className="article-title-text">
          Article {articleIdx}: {article.title}
        </div>
        <div className="article-title-date">
          <TimeAgo date={time} />
        </div>
      </div>
      <div>
        <Grid justifyContent="center" container spacing={0}>
          <Grid xs={12}>
            <Grid justifyContent="right" container spacing={0}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={isHidden}
                      onChange={handleVisibilityChange}
                      inputProps={{ 'aria-label': 'controlled' }}
                    />
                  }
                  label="Hide"
                />
              </FormGroup>
            </Grid>
          </Grid>
          <Grid md={6} xs={12}>
            <div className="article-content">{article.content.replace(/[\n]+/g, '\n\n')}</div>
          </Grid>
          <Grid md={6} xs={12}>
            <div className={isHidden ? 'article-content-hide' : 'article-content'}>
              {article.translated.replace(/[\n]+/g, '\n\n')}
            </div>
          </Grid>
        </Grid>

        <div className="article-audio">
          <ReactAudioPlayer src={article.audioObjectKey} controls />
        </div>
        <div className="article-question">Qn:&nbsp;{article.question}</div>
      </div>
      {article.options.map((option, idx) => (
        <div key={idx} className="article-option">
          <Button
            fullWidth
            variant="outlined"
            onClick={() => setUserAnswer(idx)}
            color={
              userAnswer === idx && option.is_answer
                ? 'success'
                : userAnswer === idx && !option.is_answer
                ? 'error'
                : 'info'
            }
            style={{ textTransform: 'none' }}
          >
            {idx + 1}:&nbsp;{option.option}
          </Button>
        </div>
      ))}
    </div>
  );
};

const LoadingSpinner = () => {
  return (
    <Grid direction="column" alignItems="center" justifyContent="center" container spacing={0}>
      <BounceLoader color="#36d7b7" />
    </Grid>
  );
};

const App = () => {
  const [articles, setArticles] = React.useState<ArticleType[]>([]);

  const getReadingPassages = async () => {
    const data = await fetchReadingPassages();
    if (data === undefined) {
      return;
    }
    setArticles(data);
  };

  React.useEffect(() => {
    getReadingPassages();
  }, []);

  return (
    <div>
      <div className="app-title">Reading And Listening Comprehension Practices With ChatGPT</div>
      <Box sx={{ flexGrow: 1 }}>
        <Grid direction="column" alignItems="center" justifyContent="center" container spacing={0}>
          <Grid xs={12} md={8}>
            {articles.length === 0 ? (
              <LoadingSpinner />
            ) : (
              <Article key={1} articleIdx={1} article={articles[0]} />
              // articles.map((article, idx) => (
              //   <Article key={idx} articleIdx={idx + 1} article={article} />
              // ))
            )}
          </Grid>
        </Grid>
      </Box>
    </div>
  );
};

export default App;
