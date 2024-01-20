import React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Unstable_Grid2';
import ReactAudioPlayer from 'react-audio-player';
import TimeAgo from 'react-timeago';
import moment from 'moment';
import FormControl from '@mui/material/FormControl';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';

import { ArticleProps } from './types';
import './App.css';

export const Article: React.FC<ArticleProps> = ({ articleIdx, article }) => {
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
