import { Table, Select, Tag, Typography, Divider } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import type { EmployeeWithRole, Role } from '../types';

const { Text } = Typography;

const ROLES: Role[] = ['正式淨膚師', '實習淨膚師', '儲備店長', '正式店長'];

const ROLE_COLORS: Record<Role, string> = {
  '正式淨膚師': 'blue',
  '實習淨膚師': 'green',
  '儲備店長': 'orange',
  '正式店長': 'red',
};

interface Props {
  assignments: EmployeeWithRole[];
  onChange: (assignments: EmployeeWithRole[]) => void;
}

function updateAssignment(
  assignments: EmployeeWithRole[],
  row: number,
  patch: Partial<EmployeeWithRole>
): EmployeeWithRole[] {
  return assignments.map((a) => (a.row === row ? { ...a, ...patch } : a));
}

export default function RoleAssignment({ assignments, onChange }: Props) {
  // therapistId is fixed as the employee's sequential position in Excel (1, 2, 3...)
  // and must NOT change when roles change, because mask sales in daily sheets use this number
  const handleRoleChange = (row: number, role: Role) => {
    onChange(updateAssignment(assignments, row, { role }));
  };

  const columns: ColumnsType<EmployeeWithRole> = [
    {
      title: '姓名',
      dataIndex: 'name',
      render: (name: string) => <Text strong>{name}</Text>,
    },
    {
      title: '個人業績',
      dataIndex: 'personalPerformance',
      render: (v: number) => `${v.toLocaleString()} 元`,
    },
    {
      title: '個人消耗',
      dataIndex: 'personalConsumption',
      render: (v: number) => `${v.toLocaleString()} 元`,
    },
    {
      title: '人次',
      dataIndex: 'personCount',
      render: (v: number) => Math.round(v).toLocaleString(),
    },
    {
      title: '職務',
      dataIndex: 'role',
      render: (role: Role, record: EmployeeWithRole) => (
        <Select
          value={role}
          onChange={(val) => handleRoleChange(record.row, val)}
          style={{ width: 130 }}
          options={ROLES.map((r) => ({ value: r, label: r }))}
        />
      ),
    },
    {
      title: '職務標籤',
      dataIndex: 'role',
      key: 'tag',
      render: (role: Role) => <Tag color={ROLE_COLORS[role]}>{role}</Tag>,
    },
  ];

  const formalCount = assignments.filter((e) => e.role === '正式淨膚師').length;

  return (
    <div>
      <Divider>指派職務</Divider>
      <Text type="secondary" style={{ display: 'block', marginBottom: 12 }}>
        請為每位員工選擇職務。目前正式淨膚師人數：<Text strong>{formalCount}</Text> 位
      </Text>
      <Table
        dataSource={assignments}
        columns={columns}
        rowKey="row"
        pagination={false}
        size="small"
        scroll={{ x: 'max-content' }}
      />
    </div>
  );
}
