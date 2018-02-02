using Common.Authentication.DBHandlers;
using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Development.DevConsoleApps
{
    class Program
    {
        static void Main(string[] args)
        {
            SqlQueryer db = new SqlQueryer();
            var select = db.Select("user", new Dictionary<string, string>
            {
                { "first_name", "Ian"}
            });
            Console.WriteLine(select.ToString());
        }
    }
}
