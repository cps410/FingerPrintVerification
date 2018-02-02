using Common.Authentication.DBHandlers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Common.Authentication.Models
{
    public interface IUserAccount
    {
        /// <summary>
        /// The data manager for the UserAccount model. This performs
        /// CRUD operations on the UserAccount table.
        /// </summary>
        IDbHandler<IUserAccount> Objects { get; }

        /// <summary>
        /// Checks the password guess against that stored in the
        /// database.
        /// </summary>
        /// <param name="password"></param>
        /// <returns></returns>
        bool Authenticate(string password);
    }
}
