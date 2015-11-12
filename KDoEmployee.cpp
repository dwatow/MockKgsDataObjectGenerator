#include "stdafx.h"
#include "KDoEmployee.h"
#include <algorithm>
#include <map>
#include <list>
#include <iterator>
#include <string>

using std::find;
using std::map;
using std::list;
using std::iterator;
using std::string;

const string KDoEmployee::Field_SystemKey = "SystemKey";
const string KDoEmployee::Field_SystemKeyType = "SystemKeyType";

const string KDoEmployee::Field_Id = "Id";
const string KDoEmployee::Field_ActiveFlag = "ActiveFlag";
const string KDoEmployee::Field_SomeValue = "SomeValue";

KDoEmployee::KDoEmployee():
Id("KDoEmployee_Id"),
ActiveFlag(1),
SomeValue(0.0)
{
	KDataPersistentObject::cv_SystemKey = "489DA7EA-46E8-467D-951D-092593943C01";
	cv_ClassName = "Employee";
}

KDoEmployee* KDoEmployee::CreateDoObject()
{
	return new KDoEmployee();
}

KDoEmployee* KDoEmployee::GetDoObject(string m_SystemKey)
{
	if ("489DA7EA-46E8-467D-951D-092593943C01" == m_SystemKey)
	{
		return new KDoEmployee();
	}
	else
	{
		return 0;
	}
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, string>& m_Filter)
{
	list<KDoEmployee*> curr_list;
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, list<string> >& m_Filter)
{
	list<KDoEmployee*> curr_list;
	if ((m_Filter[KDoEmployee::Field_Id].empty() || find(m_Filter[KDoEmployee::Field_Id].begin(), m_Filter[KDoEmployee::Field_Id].end(), "KDoEmployee_Id") != m_Filter[KDoEmployee::Field_Id].end()) &&
		(m_Filter[KDoEmployee::Field_ActiveFlag].empty() || find(m_Filter[KDoEmployee::Field_ActiveFlag].begin(), m_Filter[KDoEmployee::Field_ActiveFlag].end(), "1") != m_Filter[KDoEmployee::Field_ActiveFlag].end()))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(list< map<string, string> >& m_Filter)
{
	list<KDoEmployee*> curr_list;
	for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)
	{
		if (((*it)[KDoEmployee::Field_Id].empty() || (*it)[KDoEmployee::Field_Id] == "KDoEmployee_Id") &&
			((*it)[KDoEmployee::Field_ActiveFlag].empty() || (*it)[KDoEmployee::Field_ActiveFlag] == "1"))
		{
			curr_list.push_back(new KDoEmployee());
		}
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, string>& m_Filter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, list<string> >& m_Filter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	if ((m_Filter[KDoEmployee::Field_Id].empty() || find(m_Filter[KDoEmployee::Field_Id].begin(), m_Filter[KDoEmployee::Field_Id].end(), "KDoEmployee_Id") != m_Filter[KDoEmployee::Field_Id].end()) &&
		(m_Filter[KDoEmployee::Field_ActiveFlag].empty() || find(m_Filter[KDoEmployee::Field_ActiveFlag].begin(), m_Filter[KDoEmployee::Field_ActiveFlag].end(), "1") != m_Filter[KDoEmployee::Field_ActiveFlag].end()))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(list< map<string, string> >& m_Filter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)
	{
		if (((*it)[KDoEmployee::Field_Id].empty() || (*it)[KDoEmployee::Field_Id] == "KDoEmployee_Id") &&
			((*it)[KDoEmployee::Field_ActiveFlag].empty() || (*it)[KDoEmployee::Field_ActiveFlag] == "1"))
		{
			curr_list.push_back(new KDoEmployee());
		}
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsBySql(string m_SqlFilter)
{
	list<KDoEmployee*> curr_list;
	curr_list.push_back(new KDoEmployee());
	return curr_list;
}

int KDoEmployee::GetDoObjectsCountBySql(string m_SqlFilter)
{
	return 1;
}

int KDoEmployee::GetDoObjectsCountByFilter(map<string, string>& m_Filter)
{
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		return 1;
	}
	return 0;
}

int KDoEmployee::GetDoObjectsCountByFilter(map<string, list<string> >& m_Filter)
{
	if ((m_Filter[KDoEmployee::Field_Id].empty() || find(m_Filter[KDoEmployee::Field_Id].begin(), m_Filter[KDoEmployee::Field_Id].end(), "KDoEmployee_Id") != m_Filter[KDoEmployee::Field_Id].end()) &&
		(m_Filter[KDoEmployee::Field_ActiveFlag].empty() || find(m_Filter[KDoEmployee::Field_ActiveFlag].begin(), m_Filter[KDoEmployee::Field_ActiveFlag].end(), "1") != m_Filter[KDoEmployee::Field_ActiveFlag].end()))
	{
		return 1;
	}
	return 0;
}

int KDoEmployee::GetDoObjectsCountByFilter(list< map<string, string> >& m_Filter)
{
	for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)
	{
		if (((*it)[KDoEmployee::Field_Id].empty() || (*it)[KDoEmployee::Field_Id] == "KDoEmployee_Id") &&
			((*it)[KDoEmployee::Field_ActiveFlag].empty() || (*it)[KDoEmployee::Field_ActiveFlag] == "1"))
		{
			return 1;
		}
	}
	return 0;
}

int KDoEmployee::GetDoObjectsCountByFilter(map<string, string>& m_Filter, set<string>& m_LikeColumns)
{
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		return 1;
	}
	return 0;
}

int KDoEmployee::GetDoObjectsCountByFilter(map<string, list<string> >& m_Filter, set<string>& m_LikeColumns)
{
	if ((m_Filter[KDoEmployee::Field_Id].empty() || find(m_Filter[KDoEmployee::Field_Id].begin(), m_Filter[KDoEmployee::Field_Id].end(), "KDoEmployee_Id") != m_Filter[KDoEmployee::Field_Id].end()) &&
		(m_Filter[KDoEmployee::Field_ActiveFlag].empty() || find(m_Filter[KDoEmployee::Field_ActiveFlag].begin(), m_Filter[KDoEmployee::Field_ActiveFlag].end(), "1") != m_Filter[KDoEmployee::Field_ActiveFlag].end()))
	{
		return 1;
	}
	return 0;
}

int KDoEmployee::GetDoObjectsCountByFilter(list< map<string, string> >& m_Filter, set<string>& m_LikeColumns)
{
	for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)
	{
		if (((*it)[KDoEmployee::Field_Id].empty() || (*it)[KDoEmployee::Field_Id] == "KDoEmployee_Id") &&
			((*it)[KDoEmployee::Field_ActiveFlag].empty() || (*it)[KDoEmployee::Field_ActiveFlag] == "1"))
		{
			return 1;
		}
	}
	return 0;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsBySql(string m_SqlFilter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	curr_list.push_back(new KDoEmployee());
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, string>& m_Filter, set<string>& m_LikeColumns)
{
	list<KDoEmployee*> curr_list;
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, list<string> >& m_Filter, set<string>& m_LikeColumns)
{
	list<KDoEmployee*> curr_list;
	if ((m_Filter[KDoEmployee::Field_Id].empty() || find(m_Filter[KDoEmployee::Field_Id].begin(), m_Filter[KDoEmployee::Field_Id].end(), "KDoEmployee_Id") != m_Filter[KDoEmployee::Field_Id].end()) &&
		(m_Filter[KDoEmployee::Field_ActiveFlag].empty() || find(m_Filter[KDoEmployee::Field_ActiveFlag].begin(), m_Filter[KDoEmployee::Field_ActiveFlag].end(), "1") != m_Filter[KDoEmployee::Field_ActiveFlag].end()))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(list< map<string, string> >& m_Filter, set<string>& m_LikeColumns)
{
	list<KDoEmployee*> curr_list;
	for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)
	{
		if (((*it)[KDoEmployee::Field_Id].empty() || (*it)[KDoEmployee::Field_Id] == "KDoEmployee_Id") &&
			((*it)[KDoEmployee::Field_ActiveFlag].empty() || (*it)[KDoEmployee::Field_ActiveFlag] == "1"))
		{
			curr_list.push_back(new KDoEmployee());
		}
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, string>& m_Filter, set<string>& m_LikeColumns, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(map<string, list<string> >& m_Filter, set<string>& m_LikeColumns, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	if ((m_Filter[KDoEmployee::Field_Id].empty() || find(m_Filter[KDoEmployee::Field_Id].begin(), m_Filter[KDoEmployee::Field_Id].end(), "KDoEmployee_Id") != m_Filter[KDoEmployee::Field_Id].end()) &&
		(m_Filter[KDoEmployee::Field_ActiveFlag].empty() || find(m_Filter[KDoEmployee::Field_ActiveFlag].begin(), m_Filter[KDoEmployee::Field_ActiveFlag].end(), "1") != m_Filter[KDoEmployee::Field_ActiveFlag].end()))
	{
		curr_list.push_back(new KDoEmployee());
	}
	return curr_list;
}

list<KDoEmployee*> KDoEmployee::GetDoObjectsByFilter(list< map<string, string> >& m_Filter, set<string>& m_LikeColumns, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag = true)
{
	list<KDoEmployee*> curr_list;
	for (list< map<string, string> >::iterator it = m_Filter.begin(); it != m_Filter.end(); ++it)
	{
		if (((*it)[KDoEmployee::Field_Id].empty() || (*it)[KDoEmployee::Field_Id] == "KDoEmployee_Id") &&
			((*it)[KDoEmployee::Field_ActiveFlag].empty() || (*it)[KDoEmployee::Field_ActiveFlag] == "1"))
		{
			curr_list.push_back(new KDoEmployee());
		}
	}
	return curr_list;
}

KDoEmployee* KDoEmployee::GetDoObjectByFilter(map<string, string>& m_Filter)
{
	map<string, string>::iterator id_it = m_Filter.find(KDoEmployee::Field_Id);
	map<string, string>::iterator activeflag_it = m_Filter.find(KDoEmployee::Field_ActiveFlag);
	if ((id_it != m_Filter.end() || id_it->second == "KDoKDoEmployee_Id") &&
		(activeflag_it != m_Filter.end() || activeflag_it->second == "1"))
	{
		return new KDoEmployee();
	}
	return 0;
}

KDoEmployee* KDoEmployee::GetDoObjectBySql(string m_SqlFilter)
{
	return new KDoEmployee();
}