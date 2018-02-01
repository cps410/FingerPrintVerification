using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Common.Models
{
    public interface IUserAccount
    {
        /// <summary>
        /// Checks the password guess against that stored in the
        /// database.
        /// </summary>
        /// <param name="password"></param>
        /// <returns></returns>
        bool Authenticate(string password);
    }
}
