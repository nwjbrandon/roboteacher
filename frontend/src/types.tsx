export type OptionType = {
  choice: string;
  isAnswer: boolean;
  explanation: string;
};

export type ArticleType = {
  article_id: string;
  url: string;
  title: string;
  article: string;
  translatedText: string;
  question: string;
  choices: OptionType[];
  audioObjectKey: string;
  jsonObjectKey: string;
  createdAt: string;
};

export type ArticlesType = {
  articles: ArticleType[];
};

export type BodyResponse = {
  body: ArticlesType;
};

export type DataResponse = {
  data: BodyResponse;
};

export interface ArticleProps {
  articleIdx: number;
  article: ArticleType;
}
