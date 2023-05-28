#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <queue>
#include <algorithm>
#include <iomanip>
using namespace std;

#define MaxSize 4		//�������ҵ�����ڴ����
#define EMPTY -1		//�ڴ��Ϊ�ձ�ʶ
#define TOTALNUM 320	//ָ��������

typedef int InstNum;	//ָ���
typedef int PageNum;	//ҳ��
typedef int BlockNum;	//���


/*����[low, high]������ָ��*/
InstNum getRand(InstNum low, InstNum high)
{
	if (high - low == -1) { return high; }		//������ҵ��ָ����ʴ������high��lowС1������
	return (rand() % (high - low + 1) + low);
}


class Memory
{
private:
	vector<PageNum> block;		//�ڴ��
	vector<bool> visited;		//�Ƿ�ִ�й���ָ��
	queue<BlockNum> LRU_Queue;	//�������ʹ�ö���

	int runTime = 0;					//���д���
	int adjustTime = 0;					//��ҳ����
	int restInst = TOTALNUM;			//ʣ��δִ��ָ��

	void execute(string algorithm, InstNum aim);			//�����㷨ִ��һ��ָ��
	PageNum adjust(string algorithm, BlockNum &pos);		//ҳ���û�

	void displayPosMess(InstNum aim) {									//��ӡָ���ַ��Ϣ
		cout << "�����ַΪ:" << setw(3)<<aim
			 << ", ��ַ�ռ�ҳ��Ϊ:" <<setw(2)<< aim / 10
			<< ", ҳ�ڵ�" << setw(2) << aim % 10 << "��ָ��.";
	}
	void displayLoadMess(PageNum fresh, BlockNum pos, bool flag) {		//��ӡδ������ҳ����Ϣ
		cout << endl;
		if (flag) {		//�Ѿ����ڴ����
			cout << fresh << "��ҳ�Ѿ����ڴ��е�" << pos << "�ſ�����, δ������ҳ." << endl << endl;
		}
		else {			//û���ڴ����, �����ڴ��û��
			cout << fresh << "��ҳ�����ڴ��е�" << pos << "�ſ���, δ������ҳ." << endl << endl;
		}
	}
	void displayLoadMess(PageNum old, PageNum fresh, BlockNum pos) {	//��ӡ������ҳ����Ϣ
		cout << "  || �����ڴ��е�" << setw(2)<<pos 
			<< "���е�" <<setw(2)<< old 
			<< "��ҳ, �����" << setw(2) << fresh << "��ҳ." << endl << endl;
	}

public:
	Memory() = default;
	~Memory() = default;

	void Init();		//��ʼ���ڴ�
	void Simulate(string algorithm, char type);			//�����㷨��ִ��ģʽִ��ָ�� 

	int getRunTime() { return this->runTime; }			//�������д���
	int getAdjustTime() { return this->adjustTime; }	//���ص�ҳ����
	double getAdjustRate(){ return (1.0*this->adjustTime / this->runTime); }	//����ȱҳ��
};

int main(void)
{
	char method, type, operate;	//�û��㷨, ִ��ģʽ, ����

	do
	{
		/*ѡ���û��㷨*/
		cout <<
			"*********************************************************************************\n"
			"**                                                                             **\n"
			"**                             ��ѡ���û��㷨��                                **\n"
			"**                             A.       LRU                                    **\n"
			"**                             B.       FIFO                                   **\n"
			"**                                                                             **\n"
			"*********************************************************************************\n" << endl;
		cout << "����ѡ��: ";
		do
		{
			cin >> method;
			if (method != 'A' && method != 'a' && method != 'B' && method != 'b')
			{
				cout << "��������û��㷨����, ����������: ";
			}
		} while (method != 'A' && method != 'a' && method != 'B' && method != 'b');

		string algorithm = (method == 'A' || method == 'a' ? string("LRU") : string("FIFO"));

		/*ѡ��ִ��ģʽ*/
		cout <<
			"*********************************************************************************\n"
			"**                                                                             **\n"
			"**                             ��ѡ��ִ��ģʽ��                                **\n"
			"**                             A.ִ��ǰ" << TOTALNUM << "��ָ��                               **\n"
			"**                             B.ִ��������ָ��                                **\n"
			"**                                                                             **\n"
			"*********************************************************************************\n" << endl;
		cout << "����ѡ��: ";
		do
		{
			cin >> type;
			if (type != 'A' && type != 'a' && type != 'B' && type != 'b')
			{
				cout << "�������ִ��ģʽ����, ����������: ";
			}
		} while (type != 'A' && type != 'a' && type != 'B' && type != 'b');

		/*ģ��*/
		Memory myMemory;						//�����ڴ����
		myMemory.Init();						//��ʼ���ڴ�
		srand((unsigned)time(NULL));			//��ȡ���������
		myMemory.Simulate(algorithm, type);		//���ո��㷨�͸�ִ��ģʽ����ģ��
		
		cout << algorithm << "�㷨, ";
		if (type == 'A' || type == 'a') { cout << "ִ��ǰ" << TOTALNUM << "��ָ��"; }
		else { cout << "ִ��������ָ��"; }
		cout << "ģ��������: " << endl;
		cout << "======================================" << endl
			<< "��ִ��" << myMemory.getRunTime() << "��ָ��" << endl
			<< "��ҳ����Ϊ" << myMemory.getAdjustTime() << "��" << endl
			<< "ȱҳ��Ϊ" << myMemory.getAdjustRate() << endl
			<< "=======================================" << endl;


		/*ѡ����*/
		cout <<
			"*********************************************************************************\n"
			"**                                                                             **\n"
			"**                             ��ѡ���ܣ�                                    **\n"
			"**                             A.��ʼ��                                        **\n"
			"**                             B.��������                                      **\n"
			"**                                                                             **\n"
			"*********************************************************************************\n" << endl;
		cout << "����ѡ��: ";
		do
		{
			cin >> operate;
			if (operate != 'A' && operate != 'a' && operate != 'B' && operate != 'b')
			{
				cout << "������Ĺ�������, ����������: ";
			}
		} while (operate != 'A' && operate != 'a' && operate != 'B' && operate != 'b');

		if (operate == 'B' || operate == 'b') { break; }

	} while (operate!='B' && operate!='b');

		
	cout << endl << endl
		<< "********************************" << endl
		<< "* �����ҳ�洢����ʽģ����� * " << endl
		<< "********************************" << endl
		<< endl;

	system("pause");
	return 0;
}

/* ִ��һ��ָ��
 * @param {�û��㷨} algorithm
 * @param {��ִ��ָ��} aim
*/
void Memory::execute(string algorithm, InstNum aim)
{
	this->runTime++;		//�������д���

	PageNum page = aim / 10;	//����ҳ��
	BlockNum pos = 0;

	displayPosMess(aim);

	/*����ҳ�Ƿ��Ѿ����ڴ���*/
	for (pos = 0; pos < MaxSize; ++pos)
	{
		if (block[pos] == page)
		{
			displayLoadMess(page, pos, true);

			return;
		}
	}
	/*����ڴ������޿��п�*/
	for (pos = 0; pos < MaxSize; ++pos)
	{
		if (block[pos] == EMPTY)
		{
			block[pos] = page;
			displayLoadMess(page, pos, false);

			if (algorithm == string("LRU"))
			{
				LRU_Queue.push(pos);		//����ѹ���������ʹ�ö���
			}

			return;
		}
	}

	//ִ�е���˵��: 1.�ڴ�������� 2.Ҫ���е�ҳ
	PageNum old = adjust(algorithm, pos);
	block[pos] = page;
	displayLoadMess(old, page, pos);
}

/* �����ҳ
 * @returnValue {Ҫ���滻����ҳ��}
 * @param {�û��㷨} algorithm
 * @param {���������λ��} pos 
*/
PageNum Memory::adjust(string algorithm, BlockNum &pos)
{
	this->adjustTime++;		//���µ�ҳ����

	PageNum old;
	if (algorithm == "FIFO")
	{
		pos = (this->adjustTime-1) % 4;	//ȱҳ����Ϊ1, ��0���ڴ��ҳ����, ����ǰָ�����0 ���ڴ���...�Դ�����
		old = block[pos];
	}
	else if (algorithm == "LRU")
	{
		pos = LRU_Queue.front();		//ȡ����ͷԪ�� => �������ʹ�õ�ҳ��
		LRU_Queue.pop();
		LRU_Queue.push(pos);			//����ѹ���β

		old = block[pos];
	}

	return old;
}

void Memory::Init()
{
	this->block.resize(MaxSize, EMPTY);
	this->visited.resize(TOTALNUM, false);
	while (!this->LRU_Queue.empty()) { this->LRU_Queue.pop(); }

	this->runTime = 0;
	this->adjustTime = 0;
	this->restInst = TOTALNUM;
}

/* �����ҳ�洢����ʽģ��
 * @param {�û��㷨} algorithm
 * @param {�û�ѡ���ִ������} type
*/
void Memory::Simulate(string algorithm, char type)
{
	InstNum aim;
	if (type == 'A' || type == 'a')
	{
		int cnt = 0;

		//���ѡȡһ����ʼָ��
		aim = getRand(0, TOTALNUM - 1);
		execute(algorithm, aim); cnt++;
		//˳��ִ����һ��ָ��
		aim++;
		execute(algorithm, aim); cnt++;
		while (true)
		{
			if (cnt == TOTALNUM) { break; }
			//��ת��ǰ��ַ����
			aim = getRand(0, aim - 1);
			execute(algorithm, aim); cnt++;

			if (cnt == TOTALNUM) { break; }
			//˳��ִ����һ��ָ��
			aim++;
			execute(algorithm, aim); cnt++;

			if (cnt == TOTALNUM) { break; }
			//��ת�����ַ����
			aim = getRand(aim + 1, TOTALNUM - 1); 
			execute(algorithm, aim); cnt++;

			if (cnt == TOTALNUM) { break; }
			//˳��ִ����һ��ָ��
			aim++;
			execute(algorithm, aim); cnt++;
		}
	}
	else if (type == 'B' || type == 'b')
	{
		//���ѡȡһ����ʼָ��
		aim = getRand(0, TOTALNUM - 1);
		execute(algorithm, aim); 
		restInst--; visited[aim] = true;
		//˳��ִ����һ��ָ��
		aim++;
		execute(algorithm, aim);
		restInst--; visited[aim] = true;

		while (true)
		{
			if (!restInst) { break; }
			//��ת��ǰ��ַ����
			aim = getRand(0, aim - 1);
			execute(algorithm, aim);
			if (aim!=TOTALNUM && !visited[aim]) { restInst--; visited[aim] = true; }

			if (!restInst) { break; }
			//˳��ִ����һ��ָ��
			aim++;
			execute(algorithm, aim); 
			if (aim != TOTALNUM && !visited[aim]) { restInst--; visited[aim] = true; }

			if (!restInst) { break; }
			//��ת�����ַ����
			aim = getRand(aim + 1, TOTALNUM - 1);
			execute(algorithm, aim);
			if (aim != TOTALNUM && !visited[aim]) { restInst--; visited[aim] = true; }

			if (!restInst) { break; }
			//˳��ִ����һ��ָ��
			aim++;
			execute(algorithm, aim);
			if (aim != TOTALNUM && !visited[aim]) { restInst--; visited[aim] = true; }
		}
	}
}