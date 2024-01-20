import React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Unstable_Grid2';
import axios from 'axios';
import ReactAudioPlayer from 'react-audio-player';
import BounceLoader from 'react-spinners/BounceLoader';
import TimeAgo from 'react-timeago';
import moment from 'moment';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormHelperText from '@mui/material/FormHelperText';
import FormLabel from '@mui/material/FormLabel';

import './App.css';

const BACKEND_URL: string | undefined = process.env.REACT_APP_BACKEND_URL;

type OptionType = {
  option: string;
  isAnswer: boolean;
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
  const [error, setError] = React.useState(false);
  const [helperText, setHelperText] = React.useState('');

  const time = moment.utc(article.createdAt).toDate();

  const handleVisibilityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIsHidden(event.target.checked);
  };

  const updateUserAnswer = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUserAnswer(parseInt(event.target.value));
    setError(false);
    setHelperText('');
  };

  const handleSubmit = () => {
    if (article.options[userAnswer].isAnswer) {
      setHelperText('Correct');
      setError(false);
    } else {
      setHelperText('Wrong');
      setError(true);
    }
  };

  const status = userAnswer === -1 || helperText === '' ? 'info' : error ? 'error' : 'success';

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
          <ReactAudioPlayer src={article.audioObjectKey} controls style={{ height: '40px' }} />
        </div>
        <div className="article-question">Qn:&nbsp;{article.question}</div>
      </div>
      <Grid container spacing={0}>
        <FormControl error={error}>
          <RadioGroup
            aria-labelledby="demo-error-radios"
            name="quiz"
            value={userAnswer}
            onChange={updateUserAnswer}
            className="article-option"
          >
            {article.options.map((option, idx) => (
              <FormControlLabel
                className={userAnswer === idx ? `article-option-${status}` : ''}
                key={idx}
                value={idx}
                control={<Radio size="small" />}
                label={option.option}
              />
            ))}
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid justifyContent="center" container spacing={0}>
        <Button
          disabled={userAnswer === -1}
          color={status}
          type="submit"
          variant="contained"
          onClick={handleSubmit}
        >
          Check Answer
        </Button>
      </Grid>
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
  const [articleIdx, setArticleIdx] = React.useState<string>('0');

  const getReadingPassages = async () => {
    const data = await fetchReadingPassages();
    if (data === undefined) {
      return;
    }
    setArticles(data);
  };

  const updateArticle = (event: SelectChangeEvent) => {
    setArticleIdx(event.target.value);
  };

  const displayPreviousArticle = () => {
    const prevIdx = parseInt(articleIdx) - 1;
    setArticleIdx(prevIdx.toString());
  };

  const displayNextArticle = () => {
    const nextIdx = parseInt(articleIdx) + 1;
    setArticleIdx(nextIdx.toString());
  };

  React.useEffect(() => {
    getReadingPassages();
  }, []);

  const nArticles = articles.length;
  return (
    <div className="app-canvas">
      <Grid alignItems="center" justifyContent="center" container spacing={0}>
        <Grid xs={11} md={8}>
          <div className="app-title">ChatGPT Listening Comprehension</div>
        </Grid>
      </Grid>
      <div className="app-navigation">
        <Grid alignItems="center" justifyContent="center" container spacing={0}>
          <Grid xs={11} md={8}>
            <FormControl fullWidth size="small">
              <InputLabel id="demo-simple-select-label">Article</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={articleIdx}
                label="Article Index"
                onChange={updateArticle}
              >
                {articles.map((article, idx) => (
                  <MenuItem key={idx} value={idx}>
                    {idx + 1} - {article.title}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        <Grid alignItems="center" justifyContent="center" container spacing={0}>
          <Grid xs={11} md={8}>
            <Grid alignItems="center" justifyContent="center" container spacing={0}>
              <Grid xs={6}>
                <Button
                  disabled={articleIdx === '0'}
                  size="small"
                  fullWidth
                  onClick={displayPreviousArticle}
                  style={{ textTransform: 'none' }}
                >
                  Prev Article
                </Button>
              </Grid>
              <Grid xs={6}>
                <Button
                  disabled={articleIdx === (nArticles - 1).toString()}
                  size="small"
                  fullWidth
                  onClick={displayNextArticle}
                  style={{ textTransform: 'none' }}
                >
                  Next Article
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>

      <Grid direction="column" alignItems="center" justifyContent="center" container spacing={0}>
        <Grid xs={11} md={8}>
          {articles.length === 0 ? (
            <LoadingSpinner />
          ) : (
            <Article
              key={parseInt(articleIdx) + 1}
              articleIdx={parseInt(articleIdx) + 1}
              article={articles[parseInt(articleIdx)]}
            />
          )}
        </Grid>
      </Grid>
    </div>
  );
};

export default App;
