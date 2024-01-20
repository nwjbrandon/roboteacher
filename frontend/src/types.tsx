export type OptionType = {
  option: string;
  isAnswer: boolean;
};

export type ArticleType = {
  url: string;
  title: string;
  content: string;
  translated: string;
  question: string;
  options: OptionType[];
  audioObjectKey: string;
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
