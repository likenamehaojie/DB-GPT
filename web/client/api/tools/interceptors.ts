import { AxiosError } from 'axios';
import { ApiResponse, FailedTuple, SuccessTuple, ResponseType } from '../';
import { notification } from 'antd';
import { HistoryRouterProps, unstable_HistoryRouter } from 'react-router-dom';
/**
 * Response processing
 *
 * @param promise request
 * @param ignoreCodes ignore error codes
 * @returns
 */
export const apiInterceptors = <T = any, D = any>(promise: Promise<ApiResponse<T, D>>, ignoreCodes?: '*' | (number | string)[]) => {
  return promise
    .then<SuccessTuple<T, D>>((response) => {
      const { data } = response;
      if (!data) {
        throw new Error('Network Error!');
      }
      if (!data.success) {
        if (ignoreCodes === '*' || (data.err_code && ignoreCodes && ignoreCodes.includes(data.err_code))) {
          return [null, data.data, data, response];
        } else {
          notification.error({
            message: `Request error`,
            description: data?.err_msg ?? 'The interface is abnormal. Please try again later',
          });
        }
      }
      return [null, data.data, data, response];
    })
    .catch<FailedTuple<T, D>>((err: Error | AxiosError<T, D>) => {
      let errMessage = err.message;
      // @ts-ignore
      let {response:{data:{err_code}}}  = err
       // @ts-ignore
      if( "E0005" == err_code) {
        // @ts-ignore
        window.location="/login"
      }
      if (err instanceof AxiosError) {
        try {
          const { err_msg } = JSON.parse(err.request.response) as ResponseType<null>;
          err_msg && (errMessage = err_msg);
        } catch (e) {}
      }
      notification.error({
        message: `Request error`,
        description: errMessage,
      });
      return [err, null, null, null];
    });
};
