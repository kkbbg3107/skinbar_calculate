import { InboxOutlined } from '@ant-design/icons';
import { Upload, Alert, Spin } from 'antd';
import type { UploadProps } from 'antd';
import { parseExcel } from '../lib/excelParser';
import type { ExcelData } from '../types';

const { Dragger } = Upload;

interface Props {
  onParsed: (data: ExcelData) => void;
  loading: boolean;
  setLoading: (v: boolean) => void;
  error: string | null;
  setError: (v: string | null) => void;
}

export default function FileUpload({ onParsed, loading, setLoading, error, setError }: Props) {
  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    accept: '.xlsx,.xls',
    showUploadList: false,
    beforeUpload: async (file) => {
      setError(null);
      setLoading(true);
      try {
        const data = await parseExcel(file);
        onParsed(data);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : '讀取檔案失敗');
      } finally {
        setLoading(false);
      }
      return false; // prevent default upload
    },
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      <Spin spinning={loading} tip="正在讀取 Excel...">
        <Dragger {...uploadProps} style={{ padding: '24px' }}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">點擊或拖拉 Excel 檔案到此區域</p>
          <p className="ant-upload-hint">
            支援 .xlsx / .xls 格式，需包含「月報表彙整」工作表
          </p>
        </Dragger>
      </Spin>
      {error && (
        <Alert
          type="error"
          message={error}
          style={{ marginTop: 16 }}
          showIcon
        />
      )}
    </div>
  );
}
