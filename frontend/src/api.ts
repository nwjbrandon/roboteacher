import axios from 'axios';
import { DataResponse, BodyResponse, ArticleType } from './types';

const BACKEND_URL: string | undefined = process.env.REACT_APP_BACKEND_URL;

export const fetchReadingPassages = async () => {
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
