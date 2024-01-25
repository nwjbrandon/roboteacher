import React from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Unstable_Grid2';
import BounceLoader from 'react-spinners/BounceLoader';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { ArticleType } from './types';
import { Article } from './Article';
import { fetchReadingPassages } from './api';
import './App.css';

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
          <div className="app-title">Learn Reading And Listening Comprehension With ChatGPT</div>
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
                className="app-navigation-dropdown"
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
            <Grid alignItems="center" justifyContent="center" container spacing={2}>
              <Grid xs={5}>
                <Button
                  disabled={articleIdx === '0'}
                  size="small"
                  fullWidth
                  onClick={displayPreviousArticle}
                  style={{ textTransform: 'none' }}
                  variant="outlined"
                >
                  Prev Article
                </Button>
              </Grid>
              <Grid xs={5}>
                <Button
                  disabled={articleIdx === (nArticles - 1).toString()}
                  size="small"
                  fullWidth
                  onClick={displayNextArticle}
                  style={{ textTransform: 'none' }}
                  variant="outlined"
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
